#!/usr/bin/env python

import models

from django import http
from django.utils import simplejson


def skills(request):
  skills = models.HwSkill.objects.filter(is_language=False)
  skills = skills.values_list('skill_id', 'skill_name')
  skills =  [{ "id": x[0], "name": x[1]} for x in skills]
  
  return http.HttpResponse( simplejson.dumps(skills) )


def languages(request):
  skills = models.HwSkill.objects.filter(is_language=True)
  skills = skills.values_list('skill_id', 'skill_name')
  skills =  [{ "id": x[0], "name": x[1]} for x in skills]

  return http.HttpResponse( simplejson.dumps(skills) )


def tags(request):
  tags = models.HwTag.objects.all()
  tags = tags.values_list('tag_id', 'tag_name')
  tags =  [{ "id": x[0], "name": x[1]} for x in tags]

  return http.HttpResponse( simplejson.dumps(tags) )
  
def user_skills(request, user_id):
  skill_connections = models.HwSkillConnections.objects.filter(user=user_id)
  skill_connections = skill_connections.values_list('skill', flat=True)
  
  skills = models.HwSkill.objects.filter(is_language=False, skill_id__in=skill_connections)
  skills = skills.values_list('skill_id', 'skill_name')
  skills =  [{ "id": x[0], "name": x[1]} for x in skills]
  
  return http.HttpResponse( simplejson.dumps(skills) )
  
def user_languages(request, user_id):
  skill_connections = models.HwSkillConnections.objects.filter(user=user_id)
  skill_connections = skill_connections.values_list('skill', flat=True)
  
  languages = models.HwSkill.objects.filter(is_language=True, skill_id__in=skill_connections)
  languages = languages.values_list('skill_id', 'skill_name')
  languages =  [{ "id": x[0], "name": x[1]} for x in languages]
  
  return http.HttpResponse( simplejson.dumps(languages) )
  
def user_collaborators(request, user_id):
  user_connections = models.HwUserConnections.objects.filter(user=user_id)
  user_connections = user_connections.values_list('other_user', flat=True)
  
  collaborators = models.User.objects.filter(id__in=user_connections)
  collaborators = collaborators.values_list('id', 'first_name', 'last_name')
  collaborators =  [{ "id": x[0], "name": x[1]+" " +x[2]} for x in collaborators]
  
  return http.HttpResponse( simplejson.dumps(collaborators) )
  
def hunch_skills(request, hunch_id):
  skill_connections = models.HwSkillConnections.objects.filter(hunch=hunch_id)
  skill_connections = skill_connections.values_list('skill', flat=True)
  
  skills = models.HwSkill.objects.filter(is_language=False, skill_id__in=skill_connections)
  skills = skills.values_list('skill_id', 'skill_name')
  skills =  [{ "id": x[0], "name": x[1]} for x in skills]
  
  return http.HttpResponse( simplejson.dumps(skills) )
  
def hunch_languages(request, hunch_id):
  skill_connections = models.HwSkillConnections.objects.filter(hunch=hunch_id)
  skill_connections = skill_connections.values_list('skill', flat=True)
  
  languages = models.HwSkill.objects.filter(is_language=True, skill_id__in=skill_connections)
  languages = languages.values_list('skill_id', 'skill_name')
  languages =  [{ "id": x[0], "name": x[1]} for x in languages]
  
  return http.HttpResponse( simplejson.dumps(languages) )
  
def hunch_tags(request, hunch_id):
  tag_connections = models.HwTagConnections.objects.filter(hunch=hunch_id)
  tag_connections = tag_connections.values_list('tag', flat=True)
  
  tags = models.HwTag.objects.filter(tag_id__in=tag_connections)
  tags = languages.values_list('tag_id', 'tag_name')
  tags =  [{ "id": x[0], "name": x[1]} for x in tags]
  
  return http.HttpResponse( simplejson.dumps(tags) )

