#!/usr/bin/env python

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
  url(r'^home$', 'home', name='home'),
  url(r'^profile/(?P<user_id>\d+)$', 'profile', name='profile'),
  url(r'^profile$', 'profile', name='profile'),
  url(r'^signup$', 'signup', name='signup'),
  url(r'^login$', 'login', name='login'),
  (r'^logout$', 'logout_view'),
  (r'^createGroup', 'createGroup'),
  url(r'^hunches/create', 'createHunch',),
  url(r'^hunches/(?P<hunch_id>\d+)$', 'showHunch', name="showHunch"),
  url(r'^hunches/edit/(?P<hunch_id>\d+)$', 'editHunch', name="editHunch"),
  #url(r'^addEvidence', 'HunchEvidence', 'hunchEvidence'),
  (r'^invitePeople', 'invitePeople'),
  
)

urlpatterns += patterns(
  'hunchworks.json_views',
  (r'^user/(?P<user_id>\d+)/collaborators$', 'user_collaborators'),
  (r'^user/(?P<user_id>\d+)/skills/languages$', 'user_languages'),
  (r'^user/(?P<user_id>\d+)/skills/notLanguages$', 'user_skills'),
  (r'^hunch/(?P<hunch_id>\d+)/collaborators$', 'hunch_collaborators'),
  (r'^hunch/(?P<hunch_id>\d+)/skills/languages$', 'hunch_languages'),
  (r'^hunch/(?P<hunch_id>\d+)/skills/notLanguages$', 'hunch_skills'),
  (r'^hunch/(?P<hunch_id>\d+)/tags$', 'hunch_tags'),
  (r'^skills/languages', 'languages'),
  (r'^skills/notLanguages', 'skills'),
  (r'^tags', 'tags'),

)

urlpatterns += patterns(
  'hunchworks.views',
  url(r'^', 'index', name='index'),
)

