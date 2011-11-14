#!/usr/bin/env python

import re
from embedly import Embedly
from django.conf import settings


def embedly(url):
  try:
    client = Embedly(settings.EMBEDLY_KEY)
    obj = client.oembed(url)

  except:
    return None

  if obj.type == "photo":
    return '<a href="%s" class="embed"><img src="%s"></a>' % (
      obj.url, obj.url)

  return obj


def worldbank(url):
  if re.match("^http://localhost:8000/evidence/explore", url):
    return "GRAPH!"
