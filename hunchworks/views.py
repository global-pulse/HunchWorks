#!/usr/bin/python2.7
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
from django.core.urlresolvers import reverse
# This import is used to used the redirect method
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core import exceptions

from django.contrib.auth import authenticate, login as login_, logout
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def index(request):
  return render_to_response('index.html')


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

@transaction.commit_on_success
def signup(request):
  context = RequestContext(request)

  if request.method == "POST":
    data = request.POST.copy()
    data.update({'is_active':1, 'is_staff':0, 'is_superuser':0,
              'last_login':datetime.datetime.today(),
              'date_joined':datetime.datetime.today(),
              })
    auth_user_form = forms.SignUpForm(data, instance=models.User())
    hw_user_form = forms.HwUserForm(data, instance=models.HwUser())

    if auth_user_form.is_valid() and hw_user_form.is_valid():
      user = auth_user_form.save()
      user.set_password(request.POST['password'])
      user.save()
      hw_user = hw_user_form.save(commit=False)
      hw_user.user_id = user
      hw_user.save()

      for skill_name in request.POST.getlist("skill_name"):
        skill, created = models.HwSkill.objects.get_or_create(
          skill_name=skill_name,
          is_technical=0,
          is_language=0)

        skill_connection = models.HwSkillConnections.objects.create(
          skill=skill,
          user=user.get_profile(),
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
        #TODO( Chris-8-24-2011) Find something to do with thrown exception

  else:
    auth_user_form = forms.SignUpForm()
    hw_user_form = forms.HwUserForm()

  context['auth_user_form'] = auth_user_form
  context['hw_user_form'] = hw_user_form
  return render_to_response("signup.html", context)


@login_required
def home(request):
  user_id = request.user.pk
  recent_hunches = models.HwHunch.objects.filter(privacy=PrivacyLevel.OPEN).order_by("-time_modified")[:5]
  context = RequestContext(request)
  context.update({'recent_hunches': recent_hunches })
  return render_to_response('home.html', context)


@login_required
def profile(request, user_id=None):
  if not user_id:
    user_id = request.user.pk
  user = get_object_or_404(models.User, pk=user_id)
  invite_form = forms.InvitePeople()
  context = RequestContext(request)
  context.update({ "user": user, "invite_form": invite_form })
  return render_to_response('profile.html', context)


@login_required
def invitePeople(request):
  if request.method == 'POST': # If the form has been submitted...
    form = forms.InvitePeople(request.POST)
    if form.is_valid(): # All validation rules pass
      form.save()
    else:
      return HttpResponseRedirect('profile.html') # Redirect after POST
  return render_to_response('profile.html', RequestContext(request))


@login_required
def createHunch(request):
  """Create a Hunch.  Assumes HwHunch.user = request.user! """
  context = RequestContext(request)
  if request.method == 'POST':

    data = request.POST.copy()
    data.update({'creator':request.user.pk,
              'status':1,
              #'privacy':1,
              'strength':1})
    form = forms.HwHunchForm(data)
    
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/hunchworks/profile')
    else:

      form = forms.HwHunchForm(request.POST)
  else:
    form = forms.HwHunchForm()
  print request.user.pk
  context.update({ 'form':form, 'user_id': request.user.pk })
  return render_to_response('createHunch.html', context)

@login_required
def editHunch(request, hunch_id):
  """Edit a Hunch."""
  hunch = get_object_or_404(models.HwHunch, pk=hunch_id)
  if not hunch.is_editable_by(request.user):
    raise PermissionDenied

  context = RequestContext(request)
  if request.method == 'POST':
    data = request.POST.copy()
    data.update({'creator':request.user.pk, 
              'status':1,
              'privacy':1,
              'strength':1})
    form = forms.HwHunchForm(data)

    if form.is_valid():
      form.save()
      return HttpResponseRedirect('profile.html')
    else:
      form = forms.HwHunchForm(request.POST)
  else:
    form = forms.HwHunchForm(instance = hunch)
  context.update({ 'form': form, 'hunch': hunch })
  return render_to_response('editHunch.html', context)

def showHunch(request, hunch_id):
  """Show a Hunch."""
  hunch = get_object_or_404(models.HwHunch, pk=hunch_id)

  if not hunch.is_viewable_by(request.user):
    raise PermissionDenied

  context = RequestContext(request)
  context.update({ "hunch": hunch })
  return render_to_response('showHunch.html', context) 

@login_required
def createGroup(request):
  form = forms.CreateGroupForm()
  context = RequestContext(request)
  context['form'] = form;
  return render_to_response('createGroup.html', context)


@login_required
def HunchEvidence(request):
  return render_to_response('addEvidence.html')


def importFacebook(request):
  return render_to_response('importFacebook.html')


def importLinkedIn(request):
  return render_to_response('importLinkedIn.html', RequestContext(request))


def importTeamWorks(request):
  return render_to_response('importTeamWorks.html', RequestContext(request))
  

