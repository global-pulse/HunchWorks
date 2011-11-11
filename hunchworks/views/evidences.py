#!/usr/bin/env python
# encoding: utf-8

import json
import urllib
from hunchworks import forms, models
from hunchworks.utils.pagination import paginated
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django import http
from django.contrib.auth.decorators import login_required


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
  num_countries = len( country_ids )
  
  url = "http://api.worldbank.org/countries/"
  for idx, country_id in enumerate(country_ids):
    url = url + country_id 
    if idx < num_countries -1:
      url = url + ";"
  url = url + "/indicators/" + indicator_id + "?per_page=600&format=json"
  
  data = urllib.urlopen( url )
  json_objects = json.loads(data.read())

  data_refined = [
    { "date": object["date"], "value": object["value"]}
    for object in json_objects[1]
  ]

  def _extract(key):
    things = []

    for item in json_objects[1]:
      thing = item[key]
      thing["name"] = thing["value"]
      del thing["value"]

      if not thing in things:
        things.append(thing)
    
    return things

  countries = _extract("country")
  indicators = _extract("indicator")

  data_array = []
  for item in data_refined:
    new_array = []
    new_array.append( str(item["date"]) )
    if item["value"] is None:
      new_array.append( None )
    else:
      new_array.append( float(item["value"]) )
    data_array.append( new_array )
    
  data_array.reverse()
  return (indicators, countries, data_array)

@login_required
def explore(req):
  data_array = None
  indicators_prepop = []
  countries_prepop = []

  if req.method == "POST":
    form = forms.ExploreWorldBankForm(req.POST)
    if form.is_valid():
      indicators_prepop, countries_prepop, data_array = worldbank_indicators(
        req.POST["indicator"],
        req.POST["country"].split(','))

  else:
    form = forms.ExploreWorldBankForm()

  indicators_raw = urllib.urlopen("http://api.worldbank.org/indicator?format=json&per_page=6000")
  indicators_json = json.loads(indicators_raw.read())
  indicators = [{ "id": object["id"], "name": object["name"].replace(u'\xa0', u'')} for object in indicators_json[1]]
  finished_indicators = json.dumps(indicators)

  countries_raw = urllib.urlopen("http://api.worldbank.org/country?region=WLD&format=json&per_page=500")
  countries_json = json.loads(countries_raw.read())
  countries = [{ "id": object["id"], "name": object["name"].replace(u'\xa0', u'')} for object in countries_json[1]]
  finished_countries = json.dumps(countries)

  return _render(req, "explore", {
    "form": form,
    "show_graph": data_array is not None,
    "data_array": json.dumps(data_array),
    "indicators": finished_indicators,
    "indicators_prepop": json.dumps(indicators_prepop),
    "countries": finished_countries,
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