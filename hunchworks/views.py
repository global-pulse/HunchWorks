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
# This import is used to import the model form factory so that the forms
# created in forms.py can be outputted into the templates.
from django.forms.models import modelformset_factory
# This import is used to used the redirect method
from django.http import HttpResponseRedirect


def index(request):
  form = forms.SignInForm()
  context = { 'form': form }
  return render_to_response('index.html', context)

def login(request):
  form = forms.SignInForm() # An unbound form
  context = { 'form': form }
  return render_to_response('login.html', context)

def signup(request):
  context = RequestContext(request)

  if request.method == 'POST':
    form = forms.SignUpForm(request.POST)

    if form.is_valid():
      form.save()
      return HttpResponseRedirect("profile.html")

  else:
    form = forms.SignUpForm()

  context['form'] = form
  return render_to_response("signup.html", context)

def homepage(request):
  #This picks up the user located at index 1 of the users table
  user = models.HwUser.objects.get(pk=1) 
  context = {'first_name': user.first_name}
  #context = {'first_name': 'User', 'location': 'New York'}
  return render_to_response('homepage.html', context)

def profile(request, user_id):
  user = get_object_or_404(models.HwUser, pk=user_id)
  invite_form = forms.InvitePeople()

  return render_to_response('profile.html', {
    "user": user
  })


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
  return render_to_response('profile.html')

#In progress
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
@csrf_protect
def createHunch(request):
  print 'createHunch'
  if request.method != 'POST':
    print 'not post'
    form = forms.AddHunchForm()
    return render_to_response('createHunch.html', { 'form':form }, RequestContext(request))
    
  elif request.method == 'POST':
    form = forms.AddHunchForm(request.POST)
    if form.is_valid():
      form.save()
      print 'valid'
      return render_to_response('profile.html', 
                                )
    else:
      print 'not valid'
      return HttpResponseRedirect('createHunch.html')


def createGroup(request):
  return renter_to_response('createGroup.html')


def HunchEvidence(request):
  return render_to_response('addEvidence.html')


def importFacebook(request):
  return render_to_response('importFacebook.html')


def importLinkedIn(request):
  return render_to_response('importLinkedIn.html')


def importTeamWorks(request):
  return render_to_response('importTeamWorks.html')
  

