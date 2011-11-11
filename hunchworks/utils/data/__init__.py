#!/usr/bin/env python

import urllib
import json
from django.core.cache import cache


def get_json(url, timeout=86400):
  key = "get_json:%s" % url
  data = cache.get(key)

  if data is None:
    req = urllib.urlopen(url)
    data = json.loads(req.read())
    cache.set(key, data, timeout)

  return data
