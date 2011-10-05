#!/usr/bin/env python

from hunchworks.models import Hunch, HunchUser
from hunchworks.tests.helpers import TestHelpers
from django.contrib.auth.models import User
from django.test import TestCase


class HunchViewsTest(TestCase, TestHelpers):
  fixtures = ("test_users", "test_hunches")

  def test_redirect_to_all_hunches(self):
    with self.login("one"):
      resp = self.get("hunches")
      self.assertRedirects(resp, "/hunches/all")

  def test_redirect_to_my_hunches(self):
    with self.login("two"):
      resp = self.get("hunches")
      self.assertRedirects(resp, "/hunches/my")

  def test_all_hunches(self):
    with self.login("one"):
      resp = self.get("all_hunches")
      self.assertQuery(resp, "div.hunch", count=1)

  def test_my_hunches(self):
    with self.login("two"):
      resp = self.get("my_hunches")
      self.assertQuery(resp, "div.hunch", count=1)

  def test_show_hunch(self):
    with self.login("one"):
      hunch = Hunch.objects.get(pk=1)
      resp = self.get("hunch", hunch_id=hunch.pk)
      self.assertContains(resp, hunch.title)

  def test_create_hunch(self):
    with self.login("one"):
      form = self.get_form("create_hunch")
      resp = self.submit_form(form, {
        "title": "Test Create Hunch",
        "translation_language": "1",
        "description": "I have a hunch that this test is going to pass"
      })

      created_hunch = Hunch.objects.get(title="Test Create Hunch")
      self.assertRedirects(resp, created_hunch.get_absolute_url())

  def test_edit_hunch(self):
    with self.login("one"):
      old_hunch = Hunch.objects.get(pk=1)

      form = self.get_form("edit_hunch", hunch_id=1)
      resp = self.submit_form(form, {
        "title": "Test Edit Hunch"
      })

      new_hunch = Hunch.objects.get(pk=1)
      self.assertRedirects(resp, new_hunch.get_absolute_url())
      self.assertEqual(old_hunch.description, new_hunch.description)
      self.assertEqual(new_hunch.title, "Test Edit Hunch")
