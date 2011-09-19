#!/usr/bin/env python

from pyquery import PyQuery
from hunchworks.models import Group
from django.contrib.auth.models import User
from django.test import TestCase


class GroupViewsTest(TestCase):
  fixtures = ["test_users", "test_groups"]


  def _get(self, path):
    self._resp = self.client.get(path)
    self._pyquery = PyQuery(self._resp.content)
    self.assertEqual(self._resp.status_code, 200)

  def _post(self, path, data):
    self._resp = self.client.post(path, data)
    self.assertEqual(self._resp.status_code, 302)

  def _form(self, path, selector="form"):
    resp = self.client.get(path)
    pq   = PyQuery(resp.content)
    form = pq.find(selector)[0]
    return form.fields

  def _post_form(self, path, data, selector="form"):
    fields = self._form(path, selector)
    self._post(path, dict(fields, **data))


  def assertCss(self, selector, count=1):
    pq = self._pyquery(selector)
    self.assertEqual(len(pq), count)

  def setUp(self):
    self._user = User.objects.create_user("user", "a@b.com", "pass")
    self.client.login(username="user", password="pass")

  def tearDown(self):
    self.client.logout()
    self._user.delete()


  def test_get_index(self):
    self._get("/groups")
    self.assertCss("div.group", 3)

  def test_get_show(self):
    self._get("/groups/1")
    self.assertCss("div.group")

  def test_get_edit(self):
    self._get("/groups/1/edit")
    self.assertCss("form.group")

  def test_post_edit(self):
    self._post_form("/groups/1/edit", {
      "abbreviation": "Z",
      "members": "2, 3"
    })

    group = Group.objects.get(pk=1)
    self.assertEqual(group.name, "Alpha")     # unchanged
    self.assertEqual(group.abbreviation, "Z") # changed

    m_pks = set(group.members.values_list("pk", flat=True))
    self.assertEqual(m_pks, set([2, 3]))

  def test_get_new(self):
    self._get("/groups/create")
    self.assertCss("form.group")