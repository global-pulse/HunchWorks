#!/usr/bin/env python

import urllib
from hunchworks.utils.data import get_json


def _api(endpoint, **kwargs):
  params = urllib.urlencode(dict(format="json", per_page=9999, **kwargs))
  url = "http://api.worldbank.org/%s?%s" % (endpoint, params)
  return get_json(url)[1]

def _keys(record, *args):
  return dict([
    (key, record[key]) for key in args
  ])

def _id_name(record):
  return _keys(record, "id", "name")

def indicators():
  data = _api("indicators")
  return map(_id_name, data)

def countries():
  data = _api("country", region="WLD")
  return map(_id_name, data)

# .replace(u'\xa0', u'')
