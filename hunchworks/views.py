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

from django import http
# We use this function because it allows you to send an html file as a template
# and be displayed. With http response you cannot do this.
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
# This import is used to import the model form factory so that the forms
# created in forms.py can be outputted into the templates.
from django.forms.models import modelformset_factory
# This import is used to used the redirect method
from django.http import HttpResponseRedirect
from django.template import RequestContext
import datetime


def index(request):
  return render_to_response('index.html')

def login(request):
  context = RequestContext(request)
  
  if request.method == 'POST':
    form = forms.LoginForm(request.POST)
    
    if form.is_valid():
      user = models.HwUser.objects.get(username=request.POST['username'],
        password=request.POST['password'])
      if user:
        return HttpResponseRedirect(
          reverse(home, kwargs={'user_id': user.pk}))
      else:
        print "not user"
    
  form = forms.LoginForm() # An unbound form
  context = RequestContext(request)
  context.update({ 'form': form })
  return render_to_response('login.html', context)


def signup(request):
  context = RequestContext(request)

#TODO(Chris Aug-9-2011): This always goes into POST, which always
# causes the errors to be displayed. Need to figure out what is going wrong.
  if request.method == "POST":
    form = forms.SignUpForm(request.POST)

    if form.is_valid():
      skill = models.HwSkill( skill_name = request.POST['skill_name'],
        is_technical=0, is_language=0 )
      skill_connection = models.HwSkillConnections( skill_id = skill.pk, 
        user_id = user.pk, level=1 )
      user = form.save()
      skill.save()
      skill_connection.save()
      return HttpResponseRedirect(
        reverse(profile, kwargs={'user_id': user.pk}))
      
  else:
    form = forms.SignUpForm()
    
  context['form'] = form
  return render_to_response("signup.html", context)


def home(request, user_id):
  user = get_object_or_404(models.HwUser, pk=user_id)
  #This picks up the user located at index 1 of the users table
  context = RequestContext(request)
  context.update({'first_name': user.first_name})
  return render_to_response('home.html', context)


def profile(request, user_id):
  user = get_object_or_404(models.HwUser, pk=user_id)
  invite_form = forms.InvitePeople()
  context = RequestContext(request)
  context.update({ "user": user })
  return render_to_response('profile.html', context)


def invite_people(request):
  if request.method == 'POST': # If the form has been submitted...
    form = forms.InvitePeople(request.POST)
    if form.is_valid(): # All validation rules pass
      string = request.POST['invited_emails']
      invite_list = string.split(',')
      for email_input in invite_list:
        #email_form = models.EmailField(  )
        invited_user = models.HwInvitedUser( email=email_input)
        invited_user.save()
    else:
      return HttpResponseRedirect('profile.html') # Redirect after POST
  return render_to_response('profile.html', RequestContext(request))


def createHunch(request):
  """Create a Hunch.  Assumes HwHunch.user = request.user! """
  context = RequestContext(request)
  if request.method == 'POST':

    d = request.POST.copy()
    d.update({'creator':request.user.pk, 
              'time_created':datetime.datetime.today(),
              'status':1,
              'privacy':1,
              'strength':1})
    form = forms.CreateHunchForm(d)
    
    if form.is_valid():
      #print 'createHunch: valid form'
      form.save()
      #print '    valid model, too!'
      return HttpResponseRedirect('profile.html')
    else:
      #print 'createHunch: invalid form'
      #print form.errors
      #print form.non_field_errors
      form = forms.CreateHunchForm(request.POST)
  else:
    form = forms.CreateHunchForm()
  context.update({ 'form':form })
  return render_to_response('createHunch.html', context)
  

def createGroup(request):
  return render_to_response('createGroup.html')


def HunchEvidence(request):
  return render_to_response('addEvidence.html')


def importFacebook(request):
  return render_to_response('importFacebook.html')


def importLinkedIn(request):
  return render_to_response('importLinkedIn.html', RequestContext(request))


def importTeamWorks(request):
  return render_to_response('importTeamWorks.html', RequestContext(request))
  

