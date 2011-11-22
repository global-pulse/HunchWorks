#!/usr/bin/env python

from hunchworks.events import utils


class HasEvents(object):
  def create_event(self, event_type, **kwargs):
    utils.create_event(self, event_type,  **kwargs)

  def events(self):
    return utils.events_for(self)
