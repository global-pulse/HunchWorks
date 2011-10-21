#!/usr/bin/env python

from hunchworks.models import Hunch, HunchEvidence, Vote
from django.contrib.auth.models import User
from django.test import TestCase


class HunchEvidenceTest(TestCase):
  fixtures = ("test_users", "test_hunches", "test_evidences")

  def setUp(self):
    self.hunch = Hunch.objects.get(pk=1)
    self.hunch_evidence = HunchEvidence.objects.get(pk=1)
    self._user_count = 0


  # helpers

  def _next_user_count(self):
    self._user_count += 1
    return self._user_count

  def _user(self):
    return User.objects.create_user(
      "user_%s" % self._next_user_count(),
      "user@example.com",
      "password")

  def _vote(self, choice, times=1):
    for n in range(times):
      Vote.objects.create(
        hunch_evidence=self.hunch_evidence,
        user_profile=self._user().get_profile(),
        choice=choice)

  def _votes(self, strong_sups, weak_sups, neutrals, weak_refs, strong_refs):
    self._vote(+2, strong_sups)
    self._vote(+1, weak_sups)
    self._vote(0,  neutrals)
    self._vote(-1, weak_refs)
    self._vote(-2, strong_refs)


  # actual tests

  def test_neutral_evidence(self):
    self.assertEqual(self.hunch_evidence.support_text, "Neutral")

  def test_supported_evidence(self):
    self._votes(2, 10, 0, 4, 2)
    self.assertEqual(self.hunch_evidence.support_text, "Mildly Supported")

  def test_strongly_supported_evidence(self):
    self._votes(10, 4, 0, 2, 2)
    self.assertEqual(self.hunch_evidence.support_text, "Strongly Supported")

  def test_refuted_evidence(self):
    self._votes(0, 4, 0, 8, 2)
    self.assertEqual(self.hunch_evidence.support_text, "Mildly Refuted")

  def test_strongly_refuted_evidence(self):
    self._votes(0, 4, 2, 4, 12)
    self.assertEqual(self.hunch_evidence.support_text, "Strongly Refuted")