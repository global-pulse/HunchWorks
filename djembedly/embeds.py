#!/usr/bin/env python

import hashlib
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


def url2png(url):
  token = hashlib.md5("%s+%s" % (settings.URL2PNG_SECRET, url)).hexdigest()
  image_url = "http://api.url2png.com/v3/%s/%s/854x854/%s" % (settings.URL2PNG_KEY, token, url)
  return '<a href="%s" target="_blank"><img src="%s"></a>' %\
    (url, image_url)
