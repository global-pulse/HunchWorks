#!/usr/bin/env python
# Base views files for the HunchWorks application.
# Author: Auto created by DJANGO
# Date: 2011-06-1
# License:  This  program  is  free  software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the  Free Software Foundation; either version 3 of the License, or (at your
# option)  any later version. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.

import linkedin_api
import models
import forms
import datetime
from hunchworks_enums import PrivacyLevel

from django import http
from django.db import transaction
# We use this function because it allows you to send an html file as a template
# and be displayed. With http response you cannot do this.
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError
from django.core.urlresolvers import reverse
# This import is used to used the redirect method
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core import exceptions

from django.contrib.auth import authenticate, login as login_, logout
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

@login_required
def createHunch(request):
  """Create a Hunch.  Assumes HwHunch.user = request.user! """
  context = RequestContext(request)
  if request.method == 'POST':

    data = request.POST.copy()
    data.update({'creator':request.user.pk, 'status':2})
    hw_hunch_form = forms.HwHunchForm(data, instance=models.HwHunch())
    hw_evidence_form = forms.HwEvidenceForm(data, instance=models.HwEvidence())

    if hw_hunch_form.is_valid() and hw_evidence_form.is_valid():
      hw_hunch = hw_hunch_form.save()
      
      languages_required = request.POST['languages_required']
      languages_required = languages_required.split(',')
      for skill_id in languages_required:
        skill_connection = models.HwSkillConnections.objects.create(
          skill=models.HwSkill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)
      
      skills_required = request.POST['skills_required']
      skills_required = skills_required.split(',')
      for skill_id in skills_required:
        skill_connection = models.HwSkillConnections.objects.create(
          skill=models.HwSkill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)
          
      tags = request.POST['tags']
      tags = tags.split(',')
      for tag_id in tags:
        tag_connection = models.HwTagConnections.objects.create(
          tag=models.HwTag.objects.get(pk=tag_id),
          hunch=hw_hunch)
          
      hunch_collaborators = request.POST['hunch_collaborators']
      hunch_collaborators = hunch_collaborators.split(',')
      hunch_collaborators.append( request.user.pk )
      for user_id in hunch_collaborators:
        hunch_connection = models.HwHunchConnections.objects.create(
          user=models.HwUser.objects.get(pk=user_id),
          hunch=hw_hunch,
          status=0)
      
      hw_evidence = hw_evidence_form.save(commit=False)
      hw_evidence.hunch_id = hw_hunch.pk
      hw_evidence.save()
      return HttpResponseRedirect('/hunchworks/profile')
    else:
      hunch_form = forms.HwHunchForm(request.POST)
      evidence_form = forms.HwEvidenceForm(request.POST)
  else:
    hunch_form = forms.HwHunchForm()
    evidence_form = forms.HwEvidenceForm()
    
  context.update({ 'hunch_form':hunch_form, 'evidence_form':evidence_form,
    'user_id': request.user.pk })
  return render_to_response('createHunch.html', context)


@login_required
def createGroup(request):
  form = forms.CreateGroupForm()
  context = RequestContext(request)
  context['form'] = form;
  return render_to_response('createGroup.html', context)


@login_required
def editHunch(request, hunch_id):
  """Edit a Hunch."""
  hunch = get_object_or_404(models.HwHunch, pk=hunch_id)
  if not hunch.is_editable_by(request.user):
    raise PermissionDenied

  context = RequestContext(request)
  if request.method == 'POST':
    data = request.POST.copy()
    data.update({'creator':request.user.pk, 'status':2})
    hw_hunch_form = forms.HwHunchForm(data, instance = hunch)

    if hw_hunch_form.is_valid():
      hw_hunch = hw_hunch_form.save()
      
      #create new language skills for this hunch
      languages_required = request.POST['languages_required']
      languages_required = languages_required.split(',')
      for skill_id in languages_required:
        skill_connection = models.HwSkillConnections.objects.get_or_create(
          skill=models.HwSkill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)

	  #create new non language skills for this hunch
      skills_required = request.POST['skills_required']
      skills_required = skills_required.split(',')
      for skill_id in skills_required:
        skill_connection = models.HwSkillConnections.objects.get_or_create(
          skill=models.HwSkill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)

      #remove unneeded language and skills from this hunch
      skill_connections = models.HwSkillConnections.objects.filter(hunch=hw_hunch.pk)
      skills = languages_required + skills_required
      
      for skill_connection in skill_connections:
        if str(skill_connection.skill_id) not in skills:
          models.HwSkillConnections.objects.get(pk=skill_connection.pk).delete()

      #create new tags for this hunch
      tags = request.POST['tags']
      tags = tags.split(',')
      for tag_id in tags:
        tag_connection = models.HwTagConnections.objects.get_or_create(
          tag=models.HwTag.objects.get(pk=tag_id),
          hunch=hw_hunch)
        
      #remove unneeded tags from this hunch
      tag_connections = models.HwTagConnections.objects.filter(hunch=hw_hunch.pk)
      
      for tag_connection in tag_connections:
        if str(tag_connection.tag_id) not in tags:
          models.HwTagConnections.objects.get(pk=tag_connection.pk).delete()
          
      #create new collaborators for this hunch
      hunch_collaborators = request.POST['hunch_collaborators']
      hunch_collaborators = hunch_collaborators.split(',')
      hunch_collaborators.append( request.user.pk )
      for user_id in hunch_collaborators:
        hunch_connection = models.HwHunchConnections.objects.get_or_create(
          user=models.HwUser.objects.get(pk=user_id),
          hunch=hw_hunch,
          status=0)

      #remove unneeded collaborators from this hunch
      hunch_connections = models.HwHunchConnections.objects.filter(hunch=hw_hunch.pk)
      
      for hunch_connection in hunch_connections:
        if str(hunch_connection.user_id) not in hunch_collaborators:
          models.HwHunchConnections.objects.get(pk=hunch_connection.pk).delete()

      return HttpResponseRedirect('/hunchworks/profile')
    else:
      hunch_form = forms.HwHunchForm(request.POST)
  else:
    hunch_form = forms.HwHunchForm(instance = hunch)

  context.update({ 'hunch_id': hunch_id, 'user_id': request.user.pk,
    'hunch_form': hunch_form })
  return render_to_response('editHunch.html', context)


@login_required
def home(request):
  user_id = request.user.pk
  recent_hunches = models.HwHunch.objects.filter(privacy=PrivacyLevel.OPEN).order_by("-time_modified")[:5]
  context = RequestContext(request)
  context.update({'recent_hunches': recent_hunches })
  return render_to_response('home.html', context)


def index(request):
  return render_to_response('index.html')


@login_required
def invitePeople(request):
  if request.method == 'POST': # If the form has been submitted...
    form = forms.InvitePeople(request.POST)
    if form.is_valid(): # All validation rules pass
      form.save()
    else:
      return HttpResponseRedirect('profile.html') # Redirect after POST
  return render_to_response('profile.html', RequestContext(request))


def importFacebook(request):
  return render_to_response('importFacebook.html')


def importLinkedIn(request):
  return render_to_response('importLinkedIn.html', RequestContext(request))


def importTeamWorks(request):
  return render_to_response('importTeamWorks.html', RequestContext(request))


def login(request):
  context = RequestContext(request)
  
  if request.method == 'POST':
    form = forms.LoginForm(request.POST)
    print form.errors
    if form.is_valid():
      try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
          if user.is_active:
            login_(request, user)
            return HttpResponseRedirect(
              reverse(home ))
          else:
            # Disabled account error #todo
            return HttpResponseForbidden()
        else:
          # Invalid login #todo
          return HttpResponseForbidden()

      except exceptions.ObjectDoesNotExist:
        pass
        #TODO( Chris-8-16-2011) Find something to do with thrown exception
  form = forms.LoginForm() # An unbound form
  context = RequestContext(request)
  context.update({ 'form': form })
  return render_to_response('login.html', context)


def logout_view(request):
  logout(request)
  return render_to_response('index.html')


@login_required
def profile(request, user_id=None):
  if not user_id:
    user_id = request.user.pk
  user = get_object_or_404(models.User, pk=user_id)
  invite_form = forms.InvitePeople()
  context = RequestContext(request)
  context.update({ "user": user, "invite_form": invite_form })
  return render_to_response('profile.html', context)


@transaction.commit_on_success
def signup(request):
  context = RequestContext(request)

  if request.method == "POST":
    data = request.POST.copy()
    data.update({'is_active':1, 'is_staff':0, 'is_superuser':0,
              'last_login':datetime.datetime.today(),
              'date_joined':datetime.datetime.today(),
              })
    auth_user_form = forms.AuthUserForm(data, instance=models.User())
    hw_user_form = forms.HwUserForm(data, instance=models.HwUser())

    if auth_user_form.is_valid() and hw_user_form.is_valid():
      user = auth_user_form.save()
      user.set_password(request.POST['password'])
      user.save()
      #if not user.save():
      #  raise DatabaseError
      hw_user = hw_user_form.save(commit=False)
      hw_user.user_id = user
      hw_user.save()
      #if not hw_user.save():
      #  raise DatabaseError

      languages = request.POST['languages']
      languages = languages.split(',')
      for skill_id in languages:
        skill_connection = models.HwSkillConnections.objects.create(
          skill=models.HwSkill.objects.get(pk=skill_id),
          user=models.HwUser.objects.get(pk=user.pk),
          level=1)
      
      skills = request.POST['skills']
      skills = skills.split(',')
      for skill_id in skills:
        skill_connection = models.HwSkillConnections.objects.create(
          skill=models.HwSkill.objects.get(pk=skill_id),
          user=models.HwUser.objects.get(pk=user.pk),
          level=1)

      try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
          if user.is_active:
            login_(request, user)
            return HttpResponseRedirect( reverse(home ))
      except exceptions.ObjectDoesNotExist:
        pass
        #TODO(Chris:2011-8-24) Find something to do with thrown exception
    
    else:
      auth_user_form = forms.AuthUserForm(request.POST)
      hw_user_form = forms.HwUserForm(request.POST)

  else:
    auth_user_form = forms.AuthUserForm()
    hw_user_form = forms.HwUserForm()

  context['auth_user_form'] = auth_user_form
  context['hw_user_form'] = hw_user_form
  return render_to_response("signup.html", context)


def showHunch(request, hunch_id):
  """Show a Hunch."""
  hunch = get_object_or_404(models.HwHunch, pk=hunch_id)

  if not hunch.is_viewable_by(request.user):
    raise PermissionDenied

  context = RequestContext(request)
  context.update({ "hunch": hunch })
  return render_to_response('showHunch.html', context)
  

