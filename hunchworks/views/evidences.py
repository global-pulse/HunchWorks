#!/usr/bin/env python
# encoding: utf-8

import json
import urllib
from hunchworks import forms, models
from hunchworks.utils.pagination import paginated
from hunchworks.utils.data import worldbank
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django import http


def _render(req, template, more_context):
  return render_to_response(
    "evidences/" + template +".html",
    RequestContext(req, more_context)
  )

@login_required
def index(req):
  evidences = paginated(req, models.Evidence.objects.all(), 10)

  return _render(req, "index", {
    "evidences": evidences
  })

@login_required
def show(req, evidence_id):
  evidence = get_object_or_404(
    models.Evidence,
    pk=evidence_id)

  return _render(req, "show", {
    "evidence": evidence
  })

@login_required
def edit(req, evidence_id):
  evidence = get_object_or_404(
    models.Evidence,
    pk=evidence_id)

  form = forms.EvidenceForm(
    req.POST or None,
    instance=evidence)

  if form.is_valid():
    evidence = form.save()
    return redirect(evidence)

  return _render(req, "edit", {
    "evidence": evidence,
    "form": form
  })

@login_required
def create(req):
  form = forms.EvidenceForm(req.POST or None)

  if form.is_valid():
    evidence = form.save(creator=req.user.get_profile())
    return redirect(evidence)

  return _render(req, "create", {
    "form": form
  })

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

  return _render(req, "explore", {
    "form": form,
    "flat_data": json.dumps(flat_data),
    "show_graph": flat_data is not None,

    "indicators": json.dumps(worldbank.indicators()),
    "indicators_prepop": json.dumps(indicators_prepop),

    "countries": json.dumps(worldbank.countries()),
    "countries_prepop": json.dumps(countries_prepop)
  })

@login_required
def _preview(evidence):
  return render_to_string("evidences/short.html", {
    "evidence": evidence
  })

def _search_results(query_set):
  return [
    { "id": evidence.pk, "preview": _preview(evidence) }
    for evidence in query_set]

def search(req):
  query_set = models.Evidence.search(
    req.GET["q"], req.user.get_profile())

  return http.HttpResponse(
    json.dumps(_search_results(query_set)),
    content_type="application/json"
  )