#!/usr/bin/env python

from hunchworks.models import HwGroup
from noseselenium.cases import SeleniumTestCaseMixin
from django.contrib.auth.models import User
from django.test import TestCase


class GroupViewsTest(TestCase):
  def setUp(self):
    self._user = User.objects.create_user("user", "a@b.com", "pass")
    self.client.login(username="user", password="pass")

  def tearDown(self):
    self.client.logout()
    self._user.delete()

  def test_get_index(self):
    resp = self.client.get("/hunchworks/groups")
    self.assertEqual(resp.status_code, 200)

  def test_get_show(self):
    group = HwGroup.objects.create(name="Test Group")
    resp = self.client.get("/hunchworks/groups/%d" % group.pk)
    self.assertEqual(resp.status_code, 200)

  def test_get_edit(self):
    group = HwGroup.objects.create(name="Test Group")
    resp = self.client.get("/hunchworks/groups/%d/edit" % group.pk)
    self.assertEqual(resp.status_code, 200)

  def test_get_new(self):
    resp = self.client.get("/hunchworks/groups/create")
    self.assertEqual(resp.status_code, 200)


class GroupSeleniumTest(TestCase, SeleniumTestCaseMixin):
  def test_index(self):
    self.selenium.open("/hunchworks/groups")