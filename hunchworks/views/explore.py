#!/usr/bin/env python

import json
import urllib
from hunchworks import forms
from hunchworks.utils.data import worldbank
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


def _render(req, template, more_context):
  return render_to_response(
    "explore/" + template +".html",
    RequestContext(req, more_context)
  )


def worldbank_indicators(indicator_id, country_ids):
  data = worldbank.indicator(indicator_id, country_ids)

  def _extract(key):
    things = []

    for item in data:
      thing = item[key]
      thing["name"] = thing["value"]
      del thing["value"]

      if not thing in things:
        things.append(thing)

    return things

  countries = _extract("country")
  indicators = _extract("indicator")

  def _value(value):
    if value is not None:
      return float(value)

  # all_country_data will output a dictionary that looks like this:
  # { Brazil: { 2003: 10000, 2004: 11000, 2005: 12000 },
  #   China: { 2003: 12000, 2004: 14000, 2006: 16000 }
  # }
  all_country_data = {}
  country = ""
  
  for item in reversed(data):

    if country != item["country"]["name"]:
      country = item["country"]["name"]
      all_country_data[country] = {}

    all_country_data[country][item["date"]] = _value(item["value"])

  print all_country_data

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
  
  return (indicators, countries, country_keys, final_country_data)


@login_required
def explore(req):
  flat_data = None
  flat_countries = None
  indicators_prepop = []
  countries_prepop = []

  if len(req.GET):
    form = forms.ExploreWorldBankForm(req.GET)
    if form.is_valid():

      indicators_prepop, countries_prepop, flat_countries, flat_data = worldbank_indicators(
        form.cleaned_data["indicator"],
        form.cleaned_data["country"].split(','))

  else:
    form = forms.ExploreWorldBankForm()

  create_evidence_url = reverse("create_evidence") + "?" + urllib.urlencode({
    "link": req.build_absolute_uri()
  })

  return _render(req, "explore", {
    "form": form,
    "flat_data": json.dumps(flat_data),
    "flat_countries": json.dumps(flat_countries),
    "show_graph": flat_data is not None,
    "create_evidence_url": create_evidence_url,

    "indicators": json.dumps(worldbank.indicators()),
    "indicators_prepop": json.dumps(indicators_prepop),

    "countries": json.dumps(worldbank.countries()),
    "countries_prepop": json.dumps(countries_prepop)
  })