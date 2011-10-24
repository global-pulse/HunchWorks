#!/usr/bin/env python

from hunchworks.models import Hunch, HunchUser, Evidence, HunchEvidence, Vote
from hunchworks.tests.helpers import ViewTestHelpers, UnitTestHelpers
from django.test import TestCase


class HunchTest(TestCase, UnitTestHelpers):
  fixtures = ("test_users", "test_hunches")

  def setUp(self):
    self.hunch = Hunch.objects.get(pk=1)


  # helpers

  def _evidence(self, strong_sups, weak_sups, neutrals, weak_refs, strong_refs):
    evidence = Evidence.objects.create(creator=self._user().get_profile(), link="http://example.com")
    hunch_evidence = HunchEvidence.objects.create(hunch=self.hunch, evidence=evidence)
    self._vote(hunch_evidence, +2, strong_sups)
    self._vote(hunch_evidence, +1, weak_sups)
    self._vote(hunch_evidence, 0,  neutrals)
    self._vote(hunch_evidence, -1, weak_refs)
    self._vote(hunch_evidence, -2, strong_refs)

  def _vote(self, hunch_evidence, choice, times=1):
    for n in range(times):
      Vote.objects.create(
        hunch_evidence=hunch_evidence,
        user_profile=self._user().get_profile(),
        choice=choice)


  # actual tests

  def test_neutral_hunch(self):
    self.assertEqual(self.hunch.support_text, "Neutral")

  def test_supported_hunch(self):
    self._evidence(0, 2, 0, 0, 0)
    self.assertEqual(self.hunch.support_text, "Mildly Supported")

  def test_strongly_supported_evidence(self):
    self._evidence(20, 4, 0, 2, 2)
    self.assertEqual(self.hunch.support_text, "Strongly Supported")

  def test_refuted_evidence(self):
    self._evidence(0, 4, 0, 8, 2)
    self.assertEqual(self.hunch.support_text, "Mildly Refuted")

  def test_strongly_refuted_evidence(self):
    self._evidence(0, 4, 2, 4, 16)
    self.assertEqual(self.hunch.support_text, "Strongly Refuted")




class HunchViewsTest(TestCase, ViewTestHelpers):
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
      self.assertQuery(resp, "article.hunch", count=2)

  def test_my_hunches(self):
    with self.login("two"):
      resp = self.get("my_hunches")
      self.assertQuery(resp, "article.hunch", count=1)
    
  def test_get_open(self):
    with self.login("one") as profile:
      resp1 = self.get("open_hunches")
      self.assertQuery(resp1, "article.hunch", count=2)

      hunch = Hunch.objects.create(creator=profile, title="blah", description="desc", status=2, privacy=2)
      HunchUser.objects.create(user_profile=profile, hunch=hunch)
    
      resp2 = self.get("open_hunches")
      self.assertQuery(resp2, "article.hunch", count=3)

  def test_get_finished(self):
    with self.login("one") as profile:
      resp1 = self.get("finished_hunches")
      self.assertQuery(resp1, "article.hunch", count=0)

      hunch = Hunch.objects.create(creator=profile, title="blah", description="desc", status=1, privacy=2)
      HunchUser.objects.create(user_profile=profile, hunch=hunch)

      resp2 = self.get("finished_hunches")
      self.assertQuery(resp2, "article.hunch", count=1)

      hunch2 = Hunch.objects.create(creator=profile, title="blah2", description="desc2", status=0, privacy=2)
      HunchUser.objects.create(user_profile=profile, hunch=hunch2)

      resp3 = self.get("finished_hunches")
      self.assertQuery(resp3, "article.hunch", count=2)
  
  def test_show_hunch(self):
    with self.login("one"):
      hunch = Hunch.objects.get(pk=1)
      resp = self.get("hunch", hunch_id=hunch.pk)
      self.assertContains(resp, hunch.title)

  def test_create_hunch(self):
    with self.login("one"):
      get_resp = self.get("create_hunch")
      self.assertTemplateUsed(get_resp, "hunches/create.html")

      post_resp = self.submit_form(get_resp, {
        "title": "Test Create Hunch",
        "translation_language": "1",
        "description": "I have a hunch that this test is going to pass"
      })

      created_hunch = Hunch.objects.get(title="Test Create Hunch")
      self.assertRedirects(post_resp, created_hunch.get_absolute_url())

  def test_edit_hunch(self):
    with self.login("one"):
      old_hunch = Hunch.objects.get(pk=1)
      get_resp = self.get("edit_hunch", hunch_id=1)
      self.assertTemplateUsed(get_resp, "hunches/edit.html")

      post_resp = self.submit_form(get_resp, {
        "title": "Test Edit Hunch"
      })

      new_hunch = Hunch.objects.get(pk=1)
      self.assertEqual(new_hunch.title, "Test Edit Hunch")
      self.assertEqual(old_hunch.description, new_hunch.description)
      self.assertRedirects(post_resp, new_hunch.get_absolute_url())

  def test_follow_hunch(self):
    with self.login("two"):
      resp = self.get("my_hunches")
      self.assertQuery(resp, "article.hunch", count=1)

      old_hunch = Hunch.objects.get(pk=2)
      get_resp = self.get("follow_hunch", hunch_id=old_hunch.id)
 
      resp2 = self.get("my_hunches")
      self.assertQuery(resp2, "article.hunch", count=2)

  def test_unfollow_hunch(self):
    with self.login("two"):
      resp = self.get("my_hunches")
      self.assertQuery(resp, "article.hunch", count=1)

      old_hunch = Hunch.objects.get(pk=1)
      get_resp = self.get("unfollow_hunch", hunch_id=old_hunch.id)

      resp2 = self.get("my_hunches")
      self.assertQuery(resp2, "article.hunch", count=0)

#   def test_vote(self):
#     with self.login("two")
#       hunch = Hunch.objects.get(pk=1)
#       get_resp = self.get("hunch", hunch_id=hunch.pk)
#       
#       post_resp = self.submit_form(get_resp, {
#         "action": "vote",
#         "choice": 1
#       })
#       
#       vote = Vote.objects.get(pk=1)
#       
#       self.assertRedirects(post_resp, new_hunch.get_absolute_url())
#       