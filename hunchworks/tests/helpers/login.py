#!/usr/bin/env python

from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class Login(object):
  def __init__(self, testcase, username, password):
    self.testcase = testcase
    self.username = username
    self.password = password

  def __enter__(self):
    credentials = {
      "username": self.username,
      "password": self.password }

    logged_in = self.testcase.client.login(
      **credentials)

    self._user = authenticate(
      **credentials)

    self.testcase.assertTrue(
      logged_in,
      "Login (un=%r, pw=%r) failed." %
        (self.username, self.password))

    return self._user.get_profile()

  def __exit__(self, type, value, traceback):
    self.testcase.client.logout()