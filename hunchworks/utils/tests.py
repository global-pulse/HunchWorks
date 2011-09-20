#!/usr/bin/env python

from pyquery import PyQuery
from django.test import TestCase
from django.contrib.auth.models import User


class FunctionalTest(TestCase):
  def setUp(self):
    self._user = User.objects.create_user("user", "user@example.com", "pass")
    self.client.login(username="user", password="pass")

  def tearDown(self):
    self.client.logout()
    self._user.delete()

  def GET(self, path):
    self._resp = self.client.get(path)
    self._pyquery = PyQuery(self._resp.content)
    self.assertEqual(self._resp.status_code, 200)

  def POST(self, path, data):
    self._resp = self.client.post(path, data)
    self.assertEqual(self._resp.status_code, 302)

  def _form(self, path, selector="form"):
    resp = self.client.get(path)
    pq   = PyQuery(resp.content)
    form = pq.find(selector)[0]
    return form.fields

  def _post_form(self, path, data, selector="form"):
    fields = self._form(path, selector)
    self.POST(path, dict(fields, **data))

  def assertCss(self, selector, count=1):
    pq = self._pyquery(selector)
    self.assertEqual(len(pq), count)