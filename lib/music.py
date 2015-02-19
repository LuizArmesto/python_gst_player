#!/usr/bin/env python

from gi.repository import GObject

class Music(GObject.GObject):

    uri = None

    def __init__(self, uri=None):
        super(Music, self).__init__()

        self.uri = uri
