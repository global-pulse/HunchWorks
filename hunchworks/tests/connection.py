#!/usr/bin/env python

from hunchworks.models import Connection, UserProfile
from hunchworks.tests.helpers import TestHelpers
from django.contrib.auth.models import User
from django.test import TestCase


class ConnectionViewsTest(TestCase, TestHelpers):
  fixtures = ("test_users", "test_connections")

  def test_get_index(self):
    with self.login("one") as user_profile:
      resp1 = self.get("connections")
      self.assertQuery(resp1, "div.connection", 1)

      other_user = UserProfile.objects.get(pk=3)
      Connection.objects.create(user_profile=user_profile, other_user_profile=other_user)

      resp2 = self.get("connections")
      self.assertQuery(resp2, "div.connection", 2)
