#!/usr/bin/python2.7
#
# Base views files for the HunchWorks application.

import db_conn
import linkedin_api
import models

from django import http
from django.shortcuts import render_to_response


def index(request):
  return render_to_response('signupStrict.html')


def homepage(request):
  user = models.Users.objects.get(pk=1)
  context = {'firstName': user.first_name, 'location': user.location}
  return render_to_response('homepageStrict.html', context)


def profile(request):
  user = models.Users.objects.get(pk=1)
  context = {
     'firstName': user.first_name, 'lastName': user.last_name,
     'email': user.email, 'location': user.location
     }
  return render_to_response('profileStrict.html', context)


def importFacebook(request):
  return render_to_response('importFacebook.html')


def importLinkedIn(request):
  return render_to_response('importLinkedIn.html')


def importTeamWorks(request):
  return render_to_response('importTeamWorks.html')
