#!/usr/bin/env python

from hunchworks.models import Group
from hunchworks.tests.helpers import TestHelpers
from django.contrib.auth.models import User
from django.test import TestCase


class GroupViewsTest(TestCase, TestHelpers):
  fixtures = ("test_users", "test_groups", "test_hunches")

  def test_all_groups(self):
    with self.login("one"):
      resp = self.get("all_groups")
      self.assertTemplateUsed(resp, "groups/all.html")
      self.assertQuery(resp, "div.group", count=3)

  def test_my_groups(self):
    for username, c in (("one", 0), ("two", 1)):
      with self.login(username):
        resp = self.get("my_groups")
        self.assertTemplateUsed(resp, "groups/my.html")
        self.assertQuery(resp, "div.group", count=c)

  def test_show_group(self):
    with self.login("one"):
      group = Group.objects.get(pk=1)
      resp = self.get("group", group_id=group.pk)
      self.assertTemplateUsed(resp, "groups/show.html")
      self.assertEqual(resp.context["group"], group)

  def test_create_group(self):
    with self.login("one"):
      get_resp = self.get("create_group")
      self.assertTemplateUsed(get_resp, "groups/create.html")

      post_resp = self.submit_form(get_resp, {
        "name": "Test Create Group"
      })

      created_group = Group.objects.get(name="Test Create Group")
      self.assertRedirects(post_resp, created_group.get_absolute_url())

  def test_edit_group(self):
    with self.login("one"):
      old_group = Group.objects.get(pk=1)
      get_resp = self.get("edit_group", group_id=1)
      self.assertTemplateUsed(get_resp, "groups/edit.html")

      post_resp = self.submit_form(get_resp, {
        "name": "Test Edit Group"
      })

      new_group = Group.objects.get(pk=1)
      self.assertEqual(new_group.name, "Test Edit Group")
      self.assertEqual(old_group.description, new_group.description)
      self.assertRedirects(post_resp, new_group.get_absolute_url())

  def test_more_hunches(self):
    with self.login("one"):
      group = Group.objects.get(pk=1)
      resp = self.get("group_hunches", group_id=group.pk)
      self.assertTemplateUsed(resp, "groups/view_hunches.html")
      self.assertQuery(resp, "div.hunch", count=1)
