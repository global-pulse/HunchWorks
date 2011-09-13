#!/usr/bin/env python

from pyquery import PyQuery
from hunchworks.models import Group
from django.contrib.auth.models import User
from django.test import TestCase


class GroupViewsTest(TestCase):
  def _get(self, path):
    self._resp = self.client.get(path)
    self._pyquery = PyQuery(self._resp.content)
    self.assertEqual(self._resp.status_code, 200)

  def assertCss(self, selector, count=1):
    pq = self._pyquery(selector)
    self.assertEqual(len(pq), count)

  def setUp(self):
    self._user = User.objects.create_user("user", "a@b.com", "pass")
    self.client.login(username="user", password="pass")

  def tearDown(self):
    self.client.logout()
    self._user.delete()


  def test_get_index(self):
    Group.objects.create(name="Alpha")
    Group.objects.create(name="Beta")

    self._get("/hunchworks/groups")
    self.assertCss("div.group", 2)

  def test_get_show(self):
    group = Group.objects.create(name="Test Group")
    self._get("/hunchworks/groups/%d" % group.pk)

  def test_get_edit(self):
    group = Group.objects.create(name="Test Group")
    self._get("/hunchworks/groups/%d/edit" % group.pk)

  def test_get_new(self):
    self._get("/hunchworks/groups/create")