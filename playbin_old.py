import os
from gi.repository import GObject, Gtk
import gst

def on_window_destroy(window, player):
    player.set_state(gst.STATE_NULL)
    Gtk.main_quit()

def on_message(bus, message):
    print message

GObject.threads_init()

player = gst.element_factory_make("playbin2", "player")
player.props.uri = 'file://{}/file.mp3'.format(os.path.dirname(os.path.realpath(__file__)))

player.set_state(gst.STATE_PLAYING)

bus = player.get_bus()
bus.add_signal_watch()
bus.connect('message', on_message)

window = Gtk.Window()
window.connect('destroy', on_window_destroy, player)
window.set_default_size(300, 300)
window.show_all()

Gtk.main()
