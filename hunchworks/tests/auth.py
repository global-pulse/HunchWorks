#!/usr/bin/env python

from hunchworks.tests.helpers import ViewTestHelpers
from django.test import TestCase
from hunchworks.fixtures.factories import UserFactory

class AuthViewsTest(TestCase, ViewTestHelpers):

  def setUp(self):
    UserFactory(pk=1, username="one", password="sha1$46418$ec45f4354f5583a22949b6bf87e756c5da58567d")

  def test_login(self):
    resp = self.get("login")
    self.assertTemplateUsed(resp, "auth/login.html")

    post_resp = self.submit_form(resp, {
        "username": "this shouldn't work",
        "password": ""
      })

    self.assertTemplateUsed(post_resp, "auth/login.html")

    post_resp2 = self.submit_form(resp, {
        "username": "one",
        "password": "one"
      })

    self.assertRedirects(post_resp2, "/")


  def test_logout(self):
    get_resp = self.get("logout")
    self.assertRedirects(get_resp, "login")

  def test_signup(self):
    get_resp = self.get("signup")

    post_resp = self.submit_form(get_resp, {
        "username": "this shouldn't work",
        "password1": "",
        "password2": ""
      })

    self.assertTemplateUsed(post_resp, "auth/signup.html")

    post_resp2 = self.submit_form(get_resp, {
        "username": "four",
        "password1": "four",
        "password2": "four"
      })

    self.assertRedirects(post_resp2, "/")
