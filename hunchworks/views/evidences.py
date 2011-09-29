#!/usr/bin/env python
# encoding: utf-8

import json
from hunchworks import models
from django.template.loader import render_to_string
from django import http


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