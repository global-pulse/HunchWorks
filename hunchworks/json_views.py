#!/usr/bin/env python

import json
import models
import urllib
from django.shortcuts import get_object_or_404
from django import http
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template import RequestContext


def _render(req, template, more_context):
  return render_to_response(
    "evidences/" + template +".html",
    RequestContext(req, more_context)
  )

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

def worldbank_indicators(req):
  indicator_id = req.POST["indicator"]
  country_ids = req.POST["country"].split(',')
  num_countries = len( country_ids )
  
  url = "http://api.worldbank.org/countries/"
  for idx, country_id in enumerate(country_ids):
    url = url + country_id 
    if idx < num_countries -1:
      url = url + ";"
  url = url + "/indicators/" + indicator_id + "?per_page=600&format=json"
  
  data = urllib.urlopen( url )
  json_objects = json.loads(data.read())

  #this is for Json data
  #data_refined = [{ "country": object["country"]["value"], "date": object["date"], "value": object["value"]} for object in json_objects[1]]
  #return http.HttpResponse(json.dumps(data_refined))
  
  data_refined = [{ "country": object["country"]["value"], "date": object["date"], "value": object["value"]} for object in json_objects[1]]
  data_array = []
  #data_array = data_array.fromlist( data_refined )
  for item in data_refined:
    new_array = []
    new_array.append( str(item["date"]) )
    if item["value"] is None:
      new_array.append( None )
    else:
      new_array.append( float(item["value"]) )
    data_array.append( new_array )
    
  data_array.reverse()
  return _render( req, "visualization", {
    "data_array": json.dumps(data_array)
  })

  #this was before using Token Input
  #search = req.GET["q"]
  #data = urllib.urlopen("http://api.worldbank.org/indicator?format=json&per_page=50")
  #json_objects = json.loads(data.read())
  #data_refined = [{ "id": object["id"], "name": object["name"]} for object in json_objects[1] if object["name"].find(search) != -1]
  #return http.HttpResponse(json.dumps(data_refined))
