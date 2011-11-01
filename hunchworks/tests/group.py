#!/usr/bin/env python

from hunchworks.models import Group
from hunchworks.tests.helpers import ViewTestHelpers
from django.contrib.auth.models import User
from django.test import TestCase
from hunchworks.fixtures.factories import UserFactory, GroupFactory, HunchFactory, LocationFactory, UserProfileGroupFactory

class GroupViewsTest(TestCase, ViewTestHelpers):
  fixtures = ("test_hunches",)

  def setUp(self):
      LocationFactory()
      UserFactory(pk=1, username="one")
      a = UserFactory(pk=2, username="two")().userprofile_set.all()[0]
      b = GroupFactory(pk=1)()
      [GroupFactory() for x in range(2)]

      UserProfileGroupFactory(user_profile=a, group=b)

  def test_all_groups(self):
    with self.login("one"):
      resp = self.get("all_groups")
      self.assertTemplateUsed(resp, "groups/all.html")
      self.assertQuery(resp, "article.group", count=3)

  def test_my_groups(self):
    for username, c in (("one", 0), ("two", 1)):
      with self.login(username):
        resp = self.get("my_groups")
        self.assertTemplateUsed(resp, "groups/my.html")
        self.assertQuery(resp, "article.group", count=c)

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
      self.assertQuery(resp, "article.hunch", count=1)

  def test_join_group(self):
    with self.login("two"):

      group = Group.objects.get(pk=2)
      resp = self.get("join_group", group_id=group.pk)

      resp2 = self.get("my_groups")
      self.assertQuery(resp2, "article.group", count=2)

  def test_leave_group(self):
    with self.login("two"):

      group = Group.objects.get(pk=1)
      resp = self.get("leave_group", group_id=group.pk)

      resp2 = self.get("my_groups")
      self.assertQuery(resp2, "article.group", count=0)
