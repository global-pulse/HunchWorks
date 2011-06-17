#!/usr/bin/python2.7
# Helper functions for working with the LinkedIn API.
# Author: Auto created by DJANGO
# Date: 2011-6-1
# License:  This  program  is  free  software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the  Free Software Foundation; either version 3 of the License, or (at your
# option)  any later version. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.


class Error(Exception):
  pass


class LinkedInApiError(Error):
  pass


class LinkedInApiCredentials(object):
  """Class wrapping credentials for accessing the LinkedIn API for a user.

  Attributes:
    consumer_key: The client's API key.
    consumer_secret: The client's API secret.
    user_token: The user's OAuth access token.
    user_secret: The user's OAuth access token secret.
  """

  def __init__(self, consumer_key, consumer_secret, user_token, user_secret):
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.user_token = user_key
    self.user_secret = user_secret


def GetLinkedInCredentials(user):
  """Get's OAuth credentials for a user, via the LinkedIn Exchange API.

  See http://developer.linkedin.com/docs/DOC-1252 for details of how to do this.

  Args:
    user: A models.User object.

  Returns:
    A LinkedInCredentials object.
  """
  # TODO(leah): Figure out a good way to store this kind of data so it's
  # accessible, but secure. This should either be passed in via command line
  # flags from the startup scripts, or pulled out of an encrypted config file,
  # .yaml or similar. Review options once it's clear how much config data we're
  # dealing with.
  consumer_key = ''
  consumer_secret = ''

  user_token = ''
  user_secret = ''

  return LinkedInApiCredentials(
      consumer_key, consumer_secret, user_token, user_secret)


def GetUserConnections(user):
  """Returns details of the connections for a given user.

  This is retrieved via the REST API to avoid any potential data security issues
  client side.

  Args:
    user: A models.User object.
  """
  credentials = GetLinkedInCredentials(user)
  # TODO(leah): Finish this up.
