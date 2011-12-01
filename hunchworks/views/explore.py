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

  # transform worldbank-style structure into tokeninput style structure
  # { "id": 1, "value": "US" }   =>   { "id": 1, "name": "US" }
  def _format_for_tokeninput(key):
    things = []

    for item in data.copy():
      thing = item[key]
      thing["name"] = thing["value"]
      del thing["value"]

      if not thing in things:
        things.append(thing)

    return things

  countries_prepop = _format_for_tokeninput("country")
  indicators_prepop = _format_for_tokeninput("indicator")
  
  country_keys, final_country_data = worldbank.chart( data )
  
  return (indicators_prepop, countries_prepop, country_keys, final_country_data)


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