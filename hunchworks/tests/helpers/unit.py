#!/usr/bin/env python

from django.contrib.auth.models import User


class UnitTestHelpers(object):
  def _init_user_count(self):
    if not hasattr(self, "_user_count"):
      self._user_count = 0

  def _next_user_count(self):
    self._init_user_count()
    self._user_count += 1
    return self._user_count

  def _user(self):
    return User.objects.create_user(
      "user_%s" % self._next_user_count(),
      "user@example.com",
      "password")