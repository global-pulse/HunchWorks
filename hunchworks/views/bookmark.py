#!/usr/bin/env python
# encoding: utf-8

from hunchworks import models
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import get_model
from hunchworks.utils.pagination import paginated
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response
from django.template import RequestContext
from itertools import chain


def _render(req, template, more_context):
  return render_to_response(
    "bookmarks/" + template +".html",
    RequestContext(req, more_context))

@login_required
def add(req, object_type, object_id):
  model = get_model('hunchworks', object_type)
  object = get_object_or_404(model, pk=object_id)
  bookmark = models.Bookmark.bookmark_get_create(object, req.user.get_profile())
  return redirect(req.META["HTTP_REFERER"])


@login_required
def delete(req, object_type, object_id):
  model = get_model('hunchworks', object_type)
  object = get_object_or_404(model, pk=object_id)
  bookmark = models.Bookmark.bookmark_get_create(object, req.user.get_profile()).delete()
  return redirect(req.META["HTTP_REFERER"])

@login_required
def all(req):
  object_type = ContentType.objects.get_for_model(models.Group)
  bookmarked_groups = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type).values_list("object_id")
  groups = models.Group.objects.filter(id__in=bookmarked_groups)
  
  object_type2 = ContentType.objects.get_for_model(models.Hunch)
  bookmarked_hunches = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type2).values_list("object_id")
  hunches = models.Hunch.objects.filter(id__in=bookmarked_hunches)
  
  object_type3 = ContentType.objects.get_for_model(models.Album)
  bookmarked_albums = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type3).values_list("object_id")
  albums = models.Album.objects.filter(id__in=bookmarked_albums)
  
  object_type4 = ContentType.objects.get_for_model(models.Evidence)
  bookmarked_evidence = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type4).values_list("object_id")
  evidences = models.Evidence.objects.filter(id__in=bookmarked_evidence)
  
  all_items = list(chain(groups, hunches, albums, evidences))
  
  items = paginated(req, all_items, 10)
  return _render(req, "groups", {
    "items": items, "model": "group"
  })

@login_required
def groups(req):
  object_type = ContentType.objects.get_for_model(models.Group)
  bookmarked_groups = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type).values_list("object_id")
  group_ids = models.Group.objects.filter(id__in=bookmarked_groups)
  groups = paginated(req, group_ids, 10)
  return _render(req, "groups", {
    "items": groups, "model": "group"
  })

@login_required
def hunches(req):
  object_type = ContentType.objects.get_for_model(models.Hunch)
  bookmarked_hunches = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type).values_list("object_id")
  hunch_ids = models.Hunch.objects.filter(id__in=bookmarked_hunches)
  hunches = paginated(req, hunch_ids, 10)
  return _render(req, "groups", {
    "items": hunches, "model": "hunch"
  })

@login_required
def albums(req):
  object_type = ContentType.objects.get_for_model(models.Album)
  bookmarked_albums = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type).values_list("object_id")
  album_ids = models.Album.objects.filter(id__in=bookmarked_albums)
  albums = paginated(req, album_ids, 10)
  return _render(req, "groups", {
    "items": albums, "model": "album"
  })

@login_required
def evidence(req):
  object_type = ContentType.objects.get_for_model(models.Evidence)
  bookmarked_evidence = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type).values_list("object_id")
  evidence_ids = models.Evidence.objects.filter(id__in=bookmarked_evidence)
  evidences = paginated(req, evidence_ids, 10)
  return _render(req, "groups", {
    "items": evidences, "model": "evidence"
  })