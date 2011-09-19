#!/usr/bin/env python

from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',
  (r'^hunchworks/', include('hunchworks.urls')))


# In DEBUG, also serve static files and Django admin.
if settings.DEBUG:

  from django.contrib.staticfiles.urls import staticfiles_urlpatterns
  urlpatterns += staticfiles_urlpatterns()

  from django.contrib import admin
  admin.autodiscover()
  urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)))
