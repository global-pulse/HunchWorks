#!/usr/bin/env python

from django.conf.urls.defaults import *
from djembedly import views

urlpatterns = patterns(
  "djembedly.views",

  url(r"^preview$", views.preview, name="embed_preview")
)
