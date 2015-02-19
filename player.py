#!/usr/bin/env python

from gi.repository import GObject, Gtk

import gui.main

def main():
    gui.main.Window()

    GObject.threads_init()
    Gtk.main()

if __name__ == "__main__":
    main()
