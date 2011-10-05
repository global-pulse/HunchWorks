#!/usr/bin/env python

from hunchworks.models import Group
from hunchworks.tests.helpers import TestHelpers
from django.contrib.auth.models import User
from django.test import TestCase


class GroupViewsTest(TestCase, TestHelpers):
  fixtures = ("test_users", "test_groups")

  def test_all_groups(self):
    with self.login("one"):
      resp = self.get("all_groups")
      self.assertQuery(resp, "div.group", count=3)

  def test_my_groups(self):
    with self.login("two"):
      resp = self.get("my_groups")
      self.assertQuery(resp, "div.group", count=1)

  def test_show_group(self):
    with self.login("one"):
      group = Group.objects.get(pk=1)
      resp = self.get("group", group_id=group.pk)
      self.assertContains(resp, group.name)

  def test_create_group(self):
    with self.login("one"):
      form = self.get_form("create_group")
      resp = self.submit_form(form, {
        "name": "Test Create Group"
      })

      created_group = Group.objects.get(name="Test Create Group")
      self.assertRedirects(resp, created_group.get_absolute_url())

  def test_edit_group(self):
    with self.login("one"):
      old_group = Group.objects.get(pk=1)

      form = self.get_form("edit_group", group_id=1)
      resp = self.submit_form(form, {
        "name": "Test Edit Group"
      })

      new_group = Group.objects.get(pk=1)
      self.assertRedirects(resp, new_group.get_absolute_url())
      self.assertEqual(old_group.description, new_group.description)
      self.assertEqual(new_group.name, "Test Edit Group")
