#!/usr/bin/python2.7
# Base urls for the HunchWorks application.
# Author: Auto created by DJANGO
# Date: 2011-6-1
# License:  This  program  is  free  software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the  Free Software Foundation; either version 3 of the License, or (at your
# option)  any later version. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

  # Examples:
  # url(r'^$', 'hunchWorks.views.home', name='home'),
  # url(r'^hunchWorks/', include('hunchWorks.foo.urls')),

  # Uncomment the admin/doc line below to enable admin documentation:
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  # url(r'^admin/', include(admin.site.urls)),

urlpatterns = patterns(
  'hunchworks.views',
  (r'^importTeamWorks', 'importTeamWorks'),
  (r'^importLinkedIn', 'importLinkedIn'),
  (r'^importFacebook', 'importFacebook'),
  (r'^homepage', 'homepage'),
  (r'^profile', 'profile'),
  (r'^signup', 'signup'),
  (r'^signin', 'signin'),
  (r'^', 'index'),

)
