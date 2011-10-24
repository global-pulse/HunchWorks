#!/usr/bin/env python

from hunchworks.models import Connection, UserProfile
from hunchworks.tests.helpers import TestHelpers
from django.contrib.auth.models import User
from django.test import TestCase


class UsersViewsTest(TestCase, TestHelpers):
  fixtures = ("test_users", "test_connections")

  def test_get_profile(self):
    with self.login("one") as user_profile:
      get_resp = self.get("profile")
      self.assertTemplateUsed(get_resp, "users/profile.html")

  def test_get_other_profile(self):
    with self.login("one") as user_profile:
      get_resp = self.get("profile", user_id=2)
      self.assertTemplateUsed(get_resp, "users/profile.html")

  def test_get_connections(self):
    with self.login("one") as user_profile:
      resp1 = self.get("connections")
      self.assertTemplateUsed(resp1, "users/connections.html")
      self.assertQuery(resp1, "div.connection", 1)

      other_user = UserProfile.objects.get(pk=3)
      Connection.objects.create(user_profile=user_profile, other_user_profile=other_user)

      resp2 = self.get("connections")
      self.assertQuery(resp2, "div.connection", 2)

  def test_edit_profile(self):
    with self.login("one"):
      old_profile = UserProfile.objects.get(pk=1)
      get_resp = self.get("edit_profile", user_id=1)
      self.assertTemplateUsed(get_resp, "users/edit.html")

      post_resp = self.submit_form(get_resp, {
        "name": "Test Edit Profile"
      })

      new_profile = UserProfile.objects.get(pk=1)
      self.assertEqual(old_profile.email, new_profile.email)
      self.assertTemplateUsed(get_resp, "users/edit.html")

  def test_remove(self):
    with self.login("one"):
      resp1 = self.get("connections")
      self.assertTemplateUsed(resp1, "users/connections.html")
      self.assertQuery(resp1, "div.connection", 1)
      
      new_profile = UserProfile.objects.get(pk=2)
      resp2 = self.get("remove", user_id=2)
      self.assertRedirects(resp2, new_profile.get_absolute_url())

      resp3 = self.get("connections")
      self.assertTemplateUsed(resp3, "users/connections.html")
      self.assertQuery(resp3, "div.connection", 0)

  def test_connect(self):
    with self.login("one"):
      resp1 = self.get("connections")
      self.assertTemplateUsed(resp1, "users/connections.html")
      self.assertQuery(resp1, "div.connection", 1)
      
      new_profile = UserProfile.objects.get(pk=3)
      resp2 = self.get("connect", user_id=3)
      self.assertRedirects(resp2, new_profile.get_absolute_url())

      resp3 = self.get("connections")
      self.assertTemplateUsed(resp3, "users/connections.html")
      self.assertQuery(resp3, "div.connection", 2)