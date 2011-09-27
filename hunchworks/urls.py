#!/usr/bin/env python

from django.conf.urls.defaults import *
from views import auth, dashboard, evidences, groups, hunches, users

urlpatterns = patterns(
  'hunchworks.views',

  # dashboard/home/index
  url(r'^$', dashboard.dashboard, name='dashboard'),

  # auth
  url(r'^login$',       auth.login,        name='login'),
  url(r'^logout$',      auth.logout,       name="logout"),
  url(r'^signup$',      auth.signup,       name='signup'),
  url(r'^invitePeople', auth.invitePeople, name='invitePeople'),

  # users
  url(r'^profile/(?P<user_id>\d+)$', users.profile, name='profile'),
  url(r'^profile/(?P<user_id>\d+)/edit$', users.edit, name='edit_profile'),
  url(r'^profile$', users.profile, name='profile'),
  url(r'^profile/edit$', users.edit, name='edit_profile'),
  url(r'^connections$', users.connections, name='connection'),

  # groups
  url(r'^groups$',                        groups.index,  name="groups"),
  url(r'^groups/(?P<group_id>\d+)$',      groups.show,   name="group"),
  url(r'^groups/(?P<group_id>\d+)/edit$', groups.edit,   name="edit_group"),
  url(r'^groups/create',                  groups.create, name="create_group"),
  url(r'^groups/(?P<group_id>\d+)/join$', groups.join,   name="join_group"),

  # hunches
  url(r'^hunches$',                        hunches.index,  name="hunches"),
  url(r'^hunches/(?P<hunch_id>\d+)$',      hunches.show,   name="hunch"),
  url(r'^hunches/(?P<hunch_id>\d+)/edit$', hunches.edit,   name="edit_hunch"),
  url(r'^hunches/create$',                 hunches.create, name="create_hunch"),

  # evidences
  url(r'evidences/search.json', evidences.search, name="search_evidence")
)


urlpatterns += patterns(
  'hunchworks.json_views',
  (r'^user/(?P<user_id>\d+)/collaborators$', 'user_collaborators'),
  (r'^user/(?P<user_id>\d+)/languages$', 'user_languages'),
  (r'^user/(?P<user_id>\d+)/skills$', 'user_skills'),
  (r'^group/(?P<group_id>\d+)/collaborators$', 'group_collaborators'),
  (r'^hunch/(?P<hunch_id>\d+)/collaborators$', 'hunch_collaborators'),
  (r'^hunch/(?P<hunch_id>\d+)/languages$', 'hunch_languages'),
  (r'^hunch/(?P<hunch_id>\d+)/skills$', 'hunch_skills'),
  (r'^hunch/(?P<hunch_id>\d+)/tags$', 'hunch_tags'),
  (r'^skills$', 'skills'),
  (r'^languages$', 'languages'),
  (r'^tags$', 'tags'),
  (r'^collaborators$', 'collaborators'),
)
