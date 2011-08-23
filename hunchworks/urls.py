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
  #url(r'^home/(?P<user_id>\d+)$', 'home', name='home'),
  url(r'^home/$', 'home', name='home'),
  url(r'^profile/(?P<user_id>\d+)$', 'profile', name="profile"),
  url(r'^signup$', 'signup', name='signup'),
  url(r'^login$', 'login', name='login'),
  (r'^logout$', 'logout_view'),
  (r'^createGroup', 'createGroup'),
  url(r'^hunches/create', 'createHunch',),
  url(r'^hunches/(?P<hunch_id>\d+)$', 'showHunch', name="showHunch"),
  url(r'^hunches/(?P<hunch_id>\d+)$/edit', 'editHunch'),
  url(r'^addEvidence', 'HunchEvidence', 'hunchEvidence'),
  (r'^invitePeople', 'invitePeople'),
  
)

urlpatterns += patterns(
  'hunchworks.json_views',
  (r'^skills', 'skills'),
  (r'^languages', 'languages'),
  (r'^tags', 'tags'),
)

urlpatterns += patterns(
  'hunchworks.views',
  url(r'^', 'index', name='index'),
)

