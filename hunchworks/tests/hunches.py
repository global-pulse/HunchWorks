#!/usr/bin/env python

from hunchworks.models import Hunch
from django.contrib.auth.models import User
from hunchworks.utils.tests import FunctionalTest


class HunchViewsTest(FunctionalTest):
  fixtures = ["test_users", "test_hunches", "test_languages", "test_skills",
              "test_tags"]

  def setUp(self):
    self._user = User.objects.create_user("user", "a@b.com", "pass")
    self.client.login(username="user", password="pass")

  def tearDown(self):
    self.client.logout()
    self._user.delete()


  def test_get_index(self):
    self.GET("/hunches")
    self.assertCss("div.hunch", 10)

  def test_get_show(self):
    self.GET("/hunches/1")
    self.assertCss("div.hunch")

  def test_get_edit(self):
    self.GET("/hunches/1/edit")
    self.assertCss("form.hunch")

  def test_post_edit(self):
    print "here"
    self._post_form("/hunches/1/edit", {
      "description": "test2",
      "privacy": "2", 
      "skills": "2,3,4",
      "title": "test Hunch1", 
      "translation_language": "1",
      #"evidence": [u'1', u'2'],
      "languages": "1",
      "tags": "1,2",
      "user_profiles": "1,2,3"
    })

    hunch = Hunch.objects.get(pk=1)
    self.assertEqual(hunch.title, "test Hunch1")     # unchanged
    self.assertEqual(hunch.description, "test2") # changed


    #m_pks = set(hunch.members.values_list("pk", flat=True))
    #self.assertEqual(m_pks, set([2, 3]))

  def test_get_new(self):
    self.GET("/hunches/create")
    self.assertCss("form.hunch")