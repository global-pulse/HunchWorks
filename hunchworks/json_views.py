#!/usr/bin/env python

import models
from django.shortcuts import get_object_or_404
from django import http
from django.utils import simplejson


def languages(request):
  languages = models.LanguageSkill.objects.all()
  languages = languages.values_list('id', 'name')
  languages =  [{ "id": x[0], "name": x[1]} for x in languages]

  return http.HttpResponse( simplejson.dumps(languages) )


def skills(request):
  skills = models.Skill.objects.filter()
  skills = skills.values_list('id', 'name')
  skills =  [{ "id": x[0], "name": x[1]} for x in skills]
  
  return http.HttpResponse( simplejson.dumps(skills) )


def tags(request):
  tags = models.Tag.objects.all()
  tags = tags.values_list('id', 'name')
  tags =  [{ "id": x[0], "name": x[1]} for x in tags]
  return http.HttpResponse( simplejson.dumps(tags) )


def user_collaborators(request, user_id):
  user_connections = models.UserConnection.objects.filter(user=user_id)
  user_connections = user_connections.values_list('other_user', flat=True)
  
  collaborators = models.User.objects.filter(id__in=user_connections)
  collaborators = collaborators.values_list('id', 'first_name', 'last_name')
  collaborators =  [{ "id": x[0], "name": x[1]+" " +x[2]} for x in collaborators]
  
  return http.HttpResponse( simplejson.dumps(collaborators) )


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
  hunch_connections = models.HunchConnection.objects.filter(hunch=hunch_id)
  hunch_connections = hunch_connections.values_list('user', flat=True)
  
  collaborators = models.User.objects.filter(id__in=hunch_connections)
  collaborators = collaborators.values_list('id', 'first_name', 'last_name')
  collaborators =  [{ "id": x[0], "name": x[1] + ' ' + x[2]} for x in collaborators]
  
  return http.HttpResponse( simplejson.dumps(collaborators) )


def hunch_languages(request, hunch_id):
  skill_connections = models.SkillConnection.objects.filter(hunch=hunch_id)
  skill_connections = skill_connections.values_list('skill', flat=True)
  
  languages = models.Skill.objects.filter(is_language=True, skill_id__in=skill_connections)
  languages = languages.values_list('id', 'name')
  languages =  [{ "id": x[0], "name": x[1]} for x in languages]
  
  return http.HttpResponse( simplejson.dumps(languages) )

  
def hunch_skills(request, hunch_id):
  skill_connections = models.SkillConnection.objects.filter(hunch=hunch_id)
  skill_connections = skill_connections.values_list('skill', flat=True)
  
  skills = models.Skill.objects.filter(is_language=False, skill_id__in=skill_connections)
  skills = skills.values_list('id', 'name')
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