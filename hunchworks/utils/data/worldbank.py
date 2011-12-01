#!/usr/bin/env python

import json
import urllib
from hunchworks.utils.data import get_json


def _api(endpoint, **kwargs):
  params = urllib.urlencode(dict(format="json", per_page=9999, **kwargs))
  url = "http://api.worldbank.org/%s?%s" % (endpoint, params)
  return get_json(url)[1] or []

def _keys(record, *args):
  return dict([
    (key, record[key]) for key in args
  ])

def _id_name(record):
  return _keys(record, "id", "name")


# .replace(u'\xa0', u'') ???


def indicators():
  data = _api("indicators")
  return map(_id_name, data)

def countries():
  data = _api("country", region="WLD")
  return map(_id_name, data)

def indicator(indicator_code, country_codes):
  return _api("countries/%s/indicators/%s" % (
    ";".join(country_codes), indicator_code))
    
def _value(value):
  if value is not None:
    return float(value)

def chart(data):
  all_country_data = {}
  country = ""
  
  for item in reversed(data):

    if country != item["country"]["value"]:
      country = item["country"]["value"]
      all_country_data[country] = {}

    all_country_data[country][item["date"]] = _value(item["value"])

  # This will be a unique set of years across all countries in all_country_data
  final_year_set = set()

  for country in sorted(all_country_data.keys()):
  	final_year_set.update(all_country_data[country].keys())
  
  # country_keys are the unique country names for all countries in the data.
  country_keys = all_country_data.keys()
  
  # final_country_data will be an array of arrays looking like this:
  # [ ["1998", 13000, 14000], ["1999", 15000, 16000], ["2000", 17000, 20000] ]
  final_country_data = []
  for year in sorted(final_year_set):
    temp_data = [year]
    for country in country_keys:
      temp_data.append( all_country_data[country][year] )
    final_country_data.append(temp_data)

  return (country_keys, final_country_data)

def old_chart(indicator_code, country_codes):
  data = indicator(indicator_code, country_codes)

  flat_data = [
    (unicode(item["date"]), _value(item["value"]))
    for item in reversed(data)
  ]

  return flat_data
