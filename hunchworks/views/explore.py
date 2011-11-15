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

  flat_data = [
    (unicode(item["date"]), _value(item["value"]))
    for item in reversed(data)
  ]

  return (indicators, countries, flat_data)


@login_required
def explore(req):
  flat_data = None
  indicators_prepop = []
  countries_prepop = []

  if len(req.GET):
    form = forms.ExploreWorldBankForm(req.GET)
    if form.is_valid():

      indicators_prepop, countries_prepop, flat_data = worldbank_indicators(
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
    "show_graph": flat_data is not None,
    "create_evidence_url": create_evidence_url,

    "indicators": json.dumps(worldbank.indicators()),
    "indicators_prepop": json.dumps(indicators_prepop),

    "countries": json.dumps(worldbank.countries()),
    "countries_prepop": json.dumps(countries_prepop)
  })