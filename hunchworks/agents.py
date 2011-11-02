#!/usr/bin/env python
# vim: et ts=4 sw=4

class TwitterAgent(object):
    def __init__(self, name, search):
        self._name = name
        self._search = search

    def poll(self):
        print "Hello."
