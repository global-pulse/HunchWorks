#!/usr/bin/env python

from hunchworks.models import Connection, UserProfile
from django.contrib.auth.models import User
from hunchworks.utils.tests import FunctionalTest

from factoryboy import UserProfileFactory

class ConnectionViewsTest(FunctionalTest):
  fixtures = ["test_users", "test_connections"]

  def setUp(self):
    self._user = UserProfileFactory()
    self.client.login(username="user", password="pass")

  def tearDown(self):
    self.client.logout()
    self._user.delete()

  def test_get_index(self):
    self.GET("/connections")
    self.assertCss("div.connection", 2)
    other_user = UserProfile.objects.get(pk=3)
    Connection.objects.create(user_profile=self._user.get_profile(), other_user_profile=other_user)
    self.GET("/connections")
    self.assertCss("div.connection", 3)
