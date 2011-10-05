#!/usr/bin/env python

from pyquery import PyQuery
from urlparse import urlparse
#from hunchworks.tests.helpers.response import Response
from hunchworks.tests.helpers.login import Login
from django.core.urlresolvers import reverse
from django.conf import settings


class TestHelpers(object):
  def _url(self, url_name, *args, **kwargs):
    return reverse(url_name, args=args, kwargs=kwargs)

  def get(self, url_name, *args, **kwargs):
    return self.client.get(self._url(url_name, *args, **kwargs))

  def post(self, url_name, data=None, *args, **kwargs):
    return self.client.post(self._url(url_name, *args, **kwargs), data)

  def get_form(self, *args, **kwargs):
    response = self.get(*args, **kwargs)
    form = self.query(response, "form")[0]
    form._base_url = response.request["PATH_INFO"]
    return form

  def submit_form(self, form, extra_fields):
    base_fields = dict([
      (k, v if v is not None else "")
      for k, v in form.fields.items()
    ])

    return self.client.post(
      form.action or form._base_url,
      dict(base_fields, **extra_fields))

  def query(self, response, selector):
    return PyQuery(response.content)(selector)

  def login(self, username, password=None):
    return Login(self, username, password or username)

  def assertRedirectsToLogin(self, response):
    url_parts = urlparse(response['location'])
    self.assertEqual(url_parts.path, settings.LOGIN_URL)

  def assertSelector(self, response, selector, count=None, text=None, status_code=200):
    self.assertEqual(response.status_code, status_code,
        msg_prefix + "Couldn't retrieve content: Response code was %d"
        " (expected %d)" % (response.status_code, status_code))

    pq = self.query(response, selector)

    if count is not None:
      self.assertEqual(len(pq), count)

    if text is not None:
      self.assertEqual(pq.text(), text)