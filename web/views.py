#!/usr/bin/python2.7
#
# Base views files for the HunchWorks application.

import linkedin_api
import db_conn

from django import http
from django.shortcuts import render_to_response


def index(request):
  return render_to_response('signupStrict.html')


def homepage(request):
  return render_to_response(
      'homepageStrict.html', { 'firstName': db_conn.firstName,
      'location': db_conn.location })


def profile(request):
  return render_to_response(
	  'profileStrict.html', { 'firstName': db_conn.firstName,
	  'lastName': db_conn.lastName, 'email': db_conn.email,
	  'location': db_conn.location })
	  							

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
  # (Texas): Leah in PHP you can put this information in a file in the root
  # directory that users cannot ever get access to, but you can call
  # the file with imports. Then set the permissions to 400 I think, so only
  # the owner can read from it. If you don't know anything about PHP servers
  # they have a folder usually called web, where all folders are stored, but
  # the folder itself is inaccessable from a web browser.
  key = ''
  secret = ''
  return_url = 'http://localhost:8080/web'

  url = linkedin_api.GetAuthorizationUrl(key, secret, return_url)
  return http.HttpResponseRedirect(url)
