#!/usr/bin/env python

import json
import models
from django.shortcuts import get_object_or_404
from django import http
from django.utils import simplejson


def _tokens(query_set, keys=("id", "name")):
  return map(
    lambda v: dict(zip(keys, v)),
    query_set.values_list(*keys))

def _search(req, model):
  query_set = model.search(req.GET["q"], req.user.get_profile())
  return http.HttpResponse(json.dumps(_tokens(query_set)))

def _search_collab(req, model):
  query_set = model.search(req.GET["q"], req.user.get_profile())
  values_list = query_set.values_list( "other_user_profile__id", "other_user_profile__user__username")
  collaborators = [{ "id": x[0], "name": x[1]} for x in values_list]
  return http.HttpResponse(json.dumps(collaborators))
  
def locations(req):
  return _search(req, models.Location)

def tags(req):
  return _search(req, models.Tag)

def collaborators(req):
  #this we can probably refactor and include everything in _search collab in here
  return _search_collab(req, models.Connection)

def user_groups(req):
  query_set = req.user.get_profile().group_set.filter(name__icontains=req.GET["q"])
  values_list = query_set.values_list("id", "name")
  groups = [{ "id": x[0], "name": x[1]} for x in values_list]
  return http.HttpResponse(json.dumps(groups))