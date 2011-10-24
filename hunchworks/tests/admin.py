#!/usr/bin/env python

from hunchworks.tests.helpers import ViewTestHelpers
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client


class AdminViewsTest(TestCase, ViewTestHelpers):

  def test_index(self):    
    my_admin = User.objects.create_superuser('admin', 'admin@test.com', "admin")
    
    self.login(my_admin)
    #c = Client()
    
    # You'll need to log him in before you can send requests through the client
    #c.login(username=my_admin.username, password=password)
    #resp = c.get("/admin/index.html")
