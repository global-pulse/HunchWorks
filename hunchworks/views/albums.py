#!/usr/bin/env python

from hunchworks import models, forms, hunchworks_enums
from hunchworks.utils.pagination import paginated
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


def _render(req, template, more_context):
  return render_to_response(
    "albums/" + template + ".html",
    RequestContext(req, more_context))


@login_required
def index(req):
  albums = paginated(req, models.Album.objects.all(), 10)

  return _render(req, "all", {
    "albums": albums
  })

@login_required
def all(req):
  albums = paginated(req, models.Album.objects.all(), 10)

  return _render(req, "all", {
    "albums": albums
  })

@login_required
def edit(req, album_id):
  album = get_object_or_404(models.Album, pk=album_id)
  form = forms.AlbumForm(req.POST or None, instance=album)

  if form.is_valid():
    album = form.save()
    return redirect(album)

  return _render(req, "edit", {
    "album": hunch, "user": req.user,
    "form": form
  })


@login_required
def create(req):
  form = forms.AlbumForm(req.POST or None)

  if form.is_valid():
    album = form.save()
    return redirect(album)

  return _render(req, "create", {
    "form": form, "user": req.user.get_profile()
  })
  
def show(req, album_id):
  album = get_object_or_404(models.Album, pk=album_id)

  return _render(req, "show", {
    "album": album,
  })
