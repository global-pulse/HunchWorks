#!/usr/bin/env python

from django.conf.urls.defaults import *
from views import auth, dashboard, groups, hunches, users

urlpatterns = patterns(
  'hunchworks.views',

  # dashboard
  url(r'^$', dashboard.index, name='index'),
  url(r'^home$', dashboard.home, name='home'),

  # auth
  url(r'^signup$', auth.signup, name='signup'),
  url(r'^login$', auth.login, name='login'),
  url(r'^logout$', auth.logout_view),
  url(r'^invitePeople', auth.invitePeople),
  url(r'^importTeamWorks', auth.importTeamWorks),
  url(r'^importLinkedIn', auth.importLinkedIn),
  url(r'^importFacebook', auth.importFacebook),

  # users
  url(r'^profile/(?P<user_id>\d+)$', users.profile, name='profile'),
  url(r'^profile$', users.profile, name='profile'),

  #groups
  (r'^createGroup', groups.createGroup),

  # hunches
  url(r'^hunches/(?P<hunch_id>\d+)$', hunches.showHunch, name="showHunch"),
  url(r'^hunches/create', hunches.createHunch),
  url(r'^hunches/edit/(?P<hunch_id>\d+)$', hunches.editHunch, name="editHunch"),
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