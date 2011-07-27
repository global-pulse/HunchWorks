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
from django.shortcuts import render_to_response
# This import is used to import the model form factory so that the forms
# created in forms.py can be outputted into the templates.
from django.forms.models import modelformset_factory
# This import is used to used the redirect method
from django.http import HttpResponseRedirect

def index(request):
  form = forms.SignInForm()
  context = { 'form': form }
  return render_to_response('index.html', context)


def signin(request):
  form = forms.SignInForm() # An unbound form
  context = { 'form': form }
  return render_to_response('signin.html', context)


def signup(request):
  form = forms.SignUpForm() # An unbound form
  context = { 'form': form }
  return render_to_response('signup.html', context)


def homepage(request):
  #This picks up the user located at index 1 of the users table
  #user = models.User.objects.get(pk=1) 
  #context = {'first_name': user.first_name, 'location': user.location}
  context = {'first_name': 'User', 'location': 'New York'}
  return render_to_response('homepage.html', context)


def profile(request):
  if request.method == 'POST': # If the form has been submitted...
    form = forms.SignUpForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      form.save()
      #return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
      return HttpResponseRedirect('signup.html') # Redirect after POST
  user = models.Users.objects.get(pk=1)
  context = {
    'first_name': user.first_name, 'last_name': user.last_name,
    'email': user.email, 'location': user.location,
    'occupation': user.occupation,
  }
  return render_to_response('profile.html', context)


def importFacebook(request):
  return render_to_response('importFacebook.html')


def importLinkedIn(request):
  return render_to_response('importLinkedIn.html')


def importTeamWorks(request):
  return render_to_response('importTeamWorks.html')
