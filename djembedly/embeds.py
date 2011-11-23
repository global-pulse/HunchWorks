#!/usr/bin/env python

from django.conf import settings
from embedly import Embedly


def embedly(url):
  try:
    client = Embedly(settings.EMBEDLY_KEY)
    obj = client.oembed(url)

  except:
    return None

  if obj.type == "photo":
    return '<a href="%s" class="embed"><img src="%s"></a>' % (
      obj.url, obj.url)

  return None