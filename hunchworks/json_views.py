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

def languages(req):
  return _search(req, models.Language)

def skills(req):
  return _search(req, models.Skill)

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


def user_languages(request, user_id):
  skill_connections = models.SkillConnection.objects.filter(user=user_id)
  skill_connections = skill_connections.values_list('skill', flat=True)
  
  languages = models.Skill.objects.filter(is_language=True, skill_id__in=skill_connections)
  languages = languages.values_list('id', 'name')
  languages =  [{ "id": x[0], "name": x[1]} for x in languages]
  
  return http.HttpResponse( simplejson.dumps(languages) )
  
  
def user_skills(request, user_id):
  skill_connections = models.SkillConnection.objects.filter(user=user_id)
  skill_connections = skill_connections.values_list('skill', flat=True)
  
  skills = models.Skill.objects.filter(is_language=False, skill_id__in=skill_connections)
  skills = skills.values_list('id', 'name')
  skills =  [{ "id": x[0], "name": x[1]} for x in skills]
  
  return http.HttpResponse( simplejson.dumps(skills) )
  

def hunch_collaborators(request, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  collaborators = hunch.user_profiles.values_list('id', 'name')
  collaborators =  [{ "id": x[0], "name": x[1]} for x in collaborators]
  
  return http.HttpResponse( simplejson.dumps(collaborators) )


def hunch_languages(request, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  languages = hunch.languages.values_list('id', 'name')
  languages =  [{ "id": x[0], "name": x[1]} for x in languages]
  
  return http.HttpResponse( simplejson.dumps(languages) )

  
def hunch_skills(request, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  skills = hunch.skills.values_list('id', 'name')
  skills =  [{ "id": x[0], "name": x[1]} for x in skills]
  
  return http.HttpResponse( simplejson.dumps(skills) )

  
def hunch_tags(request, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  tags = hunch.tags.values_list('id', 'name')
  tags =  [{ "id": x[0], "name": x[1]} for x in tags]
  
  return http.HttpResponse( simplejson.dumps(tags) )


def group_collaborators(request, group_id):
  group_connections = models.GroupConnection.objects.filter(group=group_id)
  group_connections = group_connections.values_list('user', flat=True)
  
  collaborators = models.User.objects.filter(id__in=group_connections)
  collaborators = collaborators.values_list('id', 'first_name', 'last_name')
  collaborators =  [{ "id": x[0], "name": x[1] + ' ' + x[2]} for x in collaborators]
  
  return http.HttpResponse( simplejson.dumps(collaborators) )