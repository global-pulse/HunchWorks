#!/usr/bin/env python
# encoding: utf-8

from hunchworks import models
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import get_model

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