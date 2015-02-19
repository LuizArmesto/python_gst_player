#!/usr/bin/env python

import sys
import os
import thread
import time

from gi.repository import GObject, Gtk, Gdk

from lib.player import Player
from lib.music import Music
from lib.thread import GeneratorTask

class Window(Gtk.Window):

    position_thread = None

    def __init__(self):
        super(Window,self).__init__()
        self.set_title("Uirapuru Music Player")
        self.set_default_size(300, -1)

        vbox = Gtk.VBox()
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text('{}/../file.mp3'.format(os.path.dirname(os.path.realpath(__file__))))
        vbox.pack_start(self.entry, False, True, 0)

        hbox = Gtk.HBox()
        vbox.add(hbox)

        self.button = Gtk.Button("Start")
        self.button.connect("clicked", self.start_stop)
        hbox.add(self.button)

        self.time_label = Gtk.Label()
        self.time_label.set_text("00:00 / 00:00")
        hbox.add(self.time_label)

        self.player = Player()
        self.player.connect('playing', self._on_player_playing)
        self.player.connect('stopped', self._on_player_stopped)

        self.show_all()

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text()

            if os.path.isfile(filepath):
                music = Music('file://%s' % filepath)
                self.player.music = music
                self.player.play()
        else:
            self.player.stop()

    def do_destroy(self, *args, **kargs):
        self.player.stop()
        Gtk.main_quit()

    def _on_player_playing(self, signal, player):
        self.position_thread = GeneratorTask(self.position_generator,
                     self.set_time_label_text).start()
        self.button.set_label('Stop')

    def _on_player_stopped(self, signal, player):
        if self.position_thread:
            self.position_thread.stop()
        self.button.set_label('Start')
        self.time_label.set_text('00:00 / 00:00')

    def set_time_label_text(self, text):
        self.time_label.set_text(text)

    def position_generator(self):
        time.sleep(0.2)
        while self.player.playing:
            try:
                dur_int = self.player.duration
                dur_str = self.player.convert_ns(dur_int)
                pos_int = self.player.position
                pos_str = self.player.convert_ns(pos_int)
                yield pos_str + ' / ' + dur_str
            except:
                pass

            time.sleep(1)



