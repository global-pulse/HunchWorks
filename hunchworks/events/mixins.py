#!/usr/bin/env python

from hunchworks.events import utils


class HasEvents(object):
  def events(self):
    return utils.events_for(self)
