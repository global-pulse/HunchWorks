#!/usr/bin/env python

from hunchworks import urls as hw_urls
from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

# Use the HunchWorks app URLs as the root, with no prefix.
urlpatterns = hw_urls.urlpatterns


# In DEBUG, also serve static files and Django admin.
if settings.DEBUG:

  from django.contrib.staticfiles.urls import staticfiles_urlpatterns
  urlpatterns += staticfiles_urlpatterns()

  from django.contrib import admin
  admin.autodiscover()
  urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)))
