#!/usr/bin/env python

from hunchworks.models import Hunch, TranslationLanguage
from django.contrib.auth.models import User
from hunchworks.utils.tests import FunctionalTest


class HunchViewsTest(FunctionalTest):
  fixtures = ["test_users", "test_hunches", "test_languages", "test_skills",
              "test_tags", "test_translation_languages"]

  def setUp(self):
    self._user = User.objects.create_user("user", "a@b.com", "pass")
    self.client.login(username="user", password="pass")

  def tearDown(self):
    self.client.logout()
    self._user.delete()

  def test_get_index(self):
    resp = self.client.get("/hunches")
    self.assertEqual( resp.status_code, 302)
    
  def test_get_all(self):
    self.GET("/hunches/all")
    self.assertCss("div.hunch", 10)
    
  def test_get_my(self):
    self.GET("/hunches/my")
    self.assertCss("div.hunch", 0)
    Hunch.objects.create(creator=self._user.get_profile(), title="blah", translation_language=TranslationLanguage.objects.get(pk=1), description="desc")
    self.GET("/hunches/my")
    self.assertCss("div.hunch", 1)

  def test_get_show(self):
    self.GET("/hunches/1")
    self.assertCss("div#hunch-show")

  def test_get_edit(self):
    self.GET("/hunches/1/edit")
    self.assertCss("form.hunch")

  def test_post_edit(self):
    self._post_form("/hunches/1/edit", {
      "description": "test2",
      "privacy": "2", 
      "skills": "2,3,4",
      "title": "test Hunch1", 
      "translation_language": "1",
      #"evidence": [u'1', u'2'],
      #"languages": "1",
      #"tags": "1,2",
      #"user_profiles": "1,2,3"
    })

    hunch = Hunch.objects.get(pk=1)
    self.assertEqual(hunch.title, "test Hunch1")     # unchanged
    self.assertEqual(hunch.description, "test2") # changed


    #m_pks = set(hunch.members.values_list("pk", flat=True))
    #self.assertEqual(m_pks, set([2, 3]))

  def test_get_new(self):
    self.GET("/hunches/create")
    self.assertCss("form.hunch")