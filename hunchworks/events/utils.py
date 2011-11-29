#!/usr/bin/env python

import datetime
import pymongo
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType


def create_event(target_object, event_type, **kwargs):
  html = _render(event_type, **kwargs)

  return _collection().insert({
    "created_at": datetime.datetime.now(),
    "content_type_id": _content_type_id(target_object),
    "object_id": target_object.pk,
    "type": event_type,
    "html": html
  })


def events_for(target_object, limit=20):
  return _collection().find(spec={
      "content_type_id": _content_type_id(target_object),
      "object_id": target_object.pk
    },

    sort=[("created_at", pymongo.DESCENDING),],
    limit=limit)


def _render(event_type, **kwargs):
  return render_to_string(
    "includes/events/%s.html" % event_type,
    kwargs
  )


def _content_type_id(obj):
  return ContentType.objects.get_for_model(obj).pk


def _collection():
  return _database().events


def _database():
  return pymongo.Connection().hunchworks
