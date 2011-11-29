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
  p = req.user.get_profile()

  return _render(req, "bookmarks", {
    "bookmark_list": paginated(req, p.bookmark_set.all(), 10)
  })

@login_required
def groups(req):
  object_type = ContentType.objects.get_for_model(models.Group)
  bookmarked_groups = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type)

  return _render(req, "bookmarks", {
    "bookmark_list": paginated(req, bookmarked_groups, 10),
  })

@login_required
def hunches(req):
  object_type = ContentType.objects.get_for_model(models.Hunch)
  bookmarked_hunches = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type)

  return _render(req, "bookmarks", {
    "bookmark_list": paginated(req, bookmarked_hunches, 10)
  })

@login_required
def albums(req):
  object_type = ContentType.objects.get_for_model(models.Album)
  bookmarked_albums = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type)

  return _render(req, "bookmarks", {
    "bookmark_list": paginated(req, bookmarked_albums, 10)
  })

@login_required
def evidence(req):
  object_type = ContentType.objects.get_for_model(models.Evidence)
  bookmarked_evidence = models.Bookmark.objects.filter(user_profile=req.user.get_profile(), content_type=object_type)

  return _render(req, "bookmarks", {
    "bookmark_list": paginated(req, bookmarked_evidence, 10)
  })