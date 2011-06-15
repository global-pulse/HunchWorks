#!/usr/bin/python2.7
#
# Base views files for the HunchWorks application.

import linkedin_api

from django import http
from django.shortcuts import render_to_response


def index(request):
  return render_to_response('signupStrict.html')


def homepage(request):
  return render_to_response(
      'homepageStrict.html', { 'firstName': firstName, 'location': location })


def profile(request):
  return render_to_response('profileStrict.html')


def importFacebook(request):
  return render_to_response('importFacebook.html')


def importLinkedIn(request):
  return render_to_response('importLinkedIn.html')


def importTeamWorks(request):
  return render_to_response('importTeamWorks.html')


def AuthorizeLinkedIn(request):
  """Redirects the user to the LinkedIn API authorization page.

  Args:
    request: The Django HTTP request.

  Returns:
    A Django HTTP response containing the redirect to the API auth page.
  """
  # TODO(leah): Figure out a good way to store this kind of data so it's
  # accessible, but secure.
  key = ''
  secret = ''
  return_url = 'http://localhost:8080/web'

  url = linkedin_api.GetAuthorizationUrl(key, secret, return_url)
  return http.HttpResponseRedirect(url)
