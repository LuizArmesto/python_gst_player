import os
from gi.repository import GObject, Gtk, Gst

def on_window_destroy(window, player):
    player.set_state(Gst.State.NULL)
    Gtk.main_quit()

def on_message(bus, message):
    message = bus.pop()
    print message

GObject.threads_init()
Gst.init_check('')

player = Gst.ElementFactory.make("playbin", "player")
player.props.uri = 'file://{}/file.mp3'.format(os.path.dirname(os.path.realpath(__file__)))

player.set_state(Gst.State.PLAYING)

bus = player.get_bus()
bus.add_signal_watch()
bus.connect('message', on_message)

window = Gtk.Window()
window.connect('destroy', on_window_destroy, player)
window.set_default_size(300, 300)
window.show_all()

Gtk.main()
