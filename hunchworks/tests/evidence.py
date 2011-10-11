#!/usr/bin/env python

from hunchworks.models import Evidence
from hunchworks.tests.helpers import TestHelpers
from django.test import TestCase


class EvidenceViewsTest(TestCase, TestHelpers):
  fixtures = ("test_users", "test_hunches", "test_evidences")

  def test_index(self):
    with self.login("one"):
      resp = self.get("evidences")
      self.assertTemplateUsed(resp, "evidences/index.html")

  def test_show(self):
    with self.login("one"):
      resp = self.get("evidence", 1)
      self.assertTemplateUsed(resp, "evidences/show.html")

  def test_create(self):
    with self.login("one"):
      resp1 = self.get("create_evidence")
      self.assertTemplateUsed(resp1, "evidences/create.html")

      resp2 = self.submit_form(resp1, {
        "title": "Created Evidence",
        "link": "http://example.com"
      })

      self.assertEqual(resp2.status_code, 302)
      created_evidence = Evidence.objects.get(title="Created Evidence")
      self.assertRedirects(resp2, created_evidence.get_absolute_url())

  def test_edit(self):
    with self.login("one"):
      old_obj = Evidence.objects.get(pk=1)
      get_resp = self.get("edit_evidence", old_obj.pk)
      self.assertTemplateUsed(get_resp, "evidences/edit.html")

      post_resp = self.submit_form(get_resp, {
        "title": "Edited Evidence"
      })

      new_obj = Evidence.objects.get(pk=old_obj.pk)
      self.assertEqual(new_obj.title, "Edited Evidence")
      self.assertEqual(old_obj.description, new_obj.description)
      self.assertRedirects(post_resp, new_obj.get_absolute_url())