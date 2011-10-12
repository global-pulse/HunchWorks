#!/usr/bin/env python

from django.conf.urls.defaults import *
from views import dashboard, auth, users, groups, hunches, evidences, albums, feeds

urlpatterns = patterns(
  'hunchworks.views',

  # dashboard/home/index
  url(r'^$', dashboard.dashboard, name='dashboard'),

  # auth
  url(r'^login$',       auth.login,        name="login"),
  url(r'^logout$',      auth.logout,       name="logout"),
  url(r'^signup$',      auth.signup,       name="signup"),
  url(r'^invitePeople', auth.invitePeople, name="invitePeople"),

  # users
  url(r'^profile/(?P<user_id>\d+)$',         users.profile,     name="profile"),
  url(r'^profile/(?P<user_id>\d+)/edit$',    users.edit,        name="edit_profile"),
  url(r'^profile$',                          users.profile,     name="profile"),
  url(r'^profile/edit$',                     users.edit,        name="edit_profile"),
  url(r'^connections$',                      users.connections, name="connections"),
  url(r'^profile/(?P<user_id>\d+)/connect$', users.connect,     name='connect'),
  url(r'^profile/(?P<user_id>\d+)/remove$',  users.remove,      name='remove'),


  # groups
  url(r'^groups$',                           groups.index,    name="groups"),
  url(r'^groups/my$',                        groups.my,       name="my_groups"),
  url(r'^groups/all$',                       groups.all,      name="all_groups"),
  url(r'^groups/(?P<group_id>\d+)$',         groups.show,     name="group"),
  url(r'^groups/(?P<group_id>\d+)/edit$',    groups.edit,     name="edit_group"),
  url(r'^groups/create',                     groups.create,   name="create_group"),
  url(r'^groups/(?P<group_id>\d+)/join$',    groups.join,     name="join_group"),
  url(r'^groups/(?P<group_id>\d+)/leave$',   groups.leave,    name="leave_group"),
  url(r'^groups/(?P<group_id>\d+)/hunches$', groups.hunches,  name="group_hunches"),

  # hunches
  url(r'^hunches$',                            hunches.index,    name="hunches"),
  url(r'^hunches/my$',                         hunches.my,       name="my_hunches"),
  url(r'^hunches/all$',                        hunches.all,      name="all_hunches"),
  url(r'^hunches/finished$',                   hunches.finished, name="finished_hunches"),
  url(r'^hunches/open$',                       hunches.open,     name="open_hunches"),
  url(r'^hunches/(?P<hunch_id>\d+)$',          hunches.show,     name="hunch"),
  url(r'^hunches/(?P<hunch_id>\d+)/edit$',     hunches.edit,     name="edit_hunch"),
  url(r'^hunches/create$',                     hunches.create,   name="create_hunch"),
  url(r'^hunches/(?P<hunch_id>\d+)/follow$',   hunches.follow,   name="follow_hunch"),
  url(r'^hunches/(?P<hunch_id>\d+)/unfollow$', hunches.unfollow, name="unfollow_hunch"),
  url(r'^hunches/feed/$', feeds.RecentHunchFeed()),

  # evidences
  url(r'^evidence$',                           evidences.index,  name="evidences"),
  url(r'^evidence/(?P<evidence_id>\d+)$',      evidences.show,   name="evidence"),
  url(r'^evidence/(?P<evidence_id>\d+)/edit$', evidences.edit,   name="edit_evidence"),
  url(r'^evidence/create$',                    evidences.create, name="create_evidence"),

  url(r'^evidences/search.json$', evidences.search, name="search_evidence"),
  url(r'^evidences/feed/$', feeds.EvidencesFeed()),
  
  # albums
  url(r'^albums$',                          albums.index,    name="albums"),
  url(r'^albums/all$',                      albums.all,      name="all_albums"),
  url(r'^albums/(?P<album_id>\d+)$',        albums.show,     name="album"),
  url(r'^albums/create$',                   albums.create,   name="create_album"),
  url(r'^albums/(?P<album_id>\d+)/edit$',   albums.edit,     name="edit_album"),
)


urlpatterns += patterns(
  'hunchworks.json_views',
  (r'^user/(?P<user_id>\d+)/collaborators$', 'collaborators'),
  (r'^user/(?P<user_id>\d+)/languages$', 'user_languages'),
  (r'^user/(?P<user_id>\d+)/skills$', 'user_skills'),
  (r'^group/(?P<group_id>\d+)/collaborators$', 'group_collaborators'),
  (r'^hunch/(?P<hunch_id>\d+)/collaborators$', 'hunch_collaborators'),
  (r'^hunch/(?P<hunch_id>\d+)/languages$', 'hunch_languages'),
  (r'^hunch/(?P<hunch_id>\d+)/skills$', 'hunch_skills'),
  (r'^hunch/(?P<hunch_id>\d+)/tags$', 'hunch_tags'),
  (r'^skills$', 'skills'),
  (r'^languages$', 'languages'),
  (r'^locations$', 'locations'),
  (r'^tags$', 'tags'),
  (r'^collaborators$', 'collaborators'),
  (r'^user/groups$', 'user_groups'),
)
