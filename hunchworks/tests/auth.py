#!/usr/bin/env python

from hunchworks.tests.helpers import ViewTestHelpers
from django.test import TestCase


class AuthViewsTest(TestCase, ViewTestHelpers):
  fixtures = ("test_users",)

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