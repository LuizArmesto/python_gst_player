#!/usr/bin/env python

from gi.repository import GObject, Gst

from lib.music import Music

class PlayerError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class PlayerEmpty(PlayerError):
    def __init__(self):
        PlayerError.__init__('Error: None music to play')

class Player(GObject.GObject):
    __gsignals__ = {
        'playing': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
                        (GObject.TYPE_PYOBJECT,)),
        'stopped': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
                        (GObject.TYPE_PYOBJECT,)),
        'ended': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
                        (GObject.TYPE_PYOBJECT,))
    }

    music = GObject.property(default=None)

    def __init__(self):
        super(Player, self).__init__()

        Gst.init_check('')

        self.player = Gst.ElementFactory.make("playbin", "player")

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)

    def play(self):
        if self.music:
            self.player.props.uri = self.music.uri
            ret = self.player.set_state(Gst.State.PLAYING)
            if ret is not Gst.StateChangeReturn.FAILURE:
                self.emit('playing', self)
        else:
            raise PlayerEmpty

    def stop(self):
        ret = self.player.set_state(Gst.State.NULL)
        self.emit('stopped', self)

    @GObject.property
    def playing(self):
        for state in self.player.get_state(0):
            if isinstance(state, Gst.State) and state == Gst.State.PLAYING:
                return True
        return False

    @GObject.property
    def duration(self):
        return self.player.query_duration(Gst.Format.TIME)[1]

    @GObject.property
    def position(self):
        return self.player.query_position(Gst.Format.TIME)[1]

    @staticmethod
    def convert_ns(t):
        if not t:
            return '00:00'

        s, ns = divmod(t, 1000000000)
        m, s = divmod(s, 60)

        if m < 60:
            return "%02i:%02i" % (m, s)
        else:
            h, m = divmod(m, 60)
            return "%i:%02i:%02i" %(h, m, s)

    def _on_message(self, bus, message):
        print message
        if message is None:
            return
        msg_type = message.type
        if msg_type == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.emit('ended', self)
        elif msg_type == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            raise PlayerError("Error: %s %s" % (err, debug))
