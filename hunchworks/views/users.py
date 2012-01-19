#!/usr/bin/env python
# encoding: utf-8

from hunchworks import models, forms
from hunchworks.utils.uploads import handle_uploaded_file
from hunchworks.utils.pagination import paginated
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def _render(req, template, more_context):
  return render_to_response(
    "users/" + template +".html",
    RequestContext(req, more_context))

@login_required
def profile(req, user_id):
  user_profile = get_object_or_404(models.UserProfile, pk=user_id)
  is_me = (req.user.get_profile() == user_profile)

  return _render(req, "profile", {
    "user_profile": user_profile,
    "hunches": user_profile.hunch_set.all(),
    "is_me": is_me
  })

@login_required
def edit(req, user_id):
  user_profile = get_object_or_404(models.UserProfile, pk=user_id)

  # Users can only edit their own profile.
  if req.user.get_profile() != user_profile:
    return HttpResponse(status=403)

  form = forms.UserForm(
    req.POST or None,
    req.FILES or None,
    instance=user_profile)

  if form.is_valid():
    for f in req.FILES:
      handle_uploaded_file(req.FILES[f], "profile_images")

    user_profile = form.save(commit=False)
    user_profile.user = req.user
    user_profile.save()

    return redirect(user_profile)

  return _render(req, "edit", {
    "form": form
  })


@login_required
def connections(req):
  return _render(req, "connections", {
    "connection_list": paginated(req, req.user.get_profile().connections.all(), 20)
  })


@login_required
def connect(req, user_id):
  user = get_object_or_404(models.UserProfile, pk=user_id)

  connection = models.Connection.objects.get_or_create(
    user_profile = req.user.get_profile(),
	other_user_profile = user,
	status=0)
  
  return redirect( user )
  
@login_required
def remove(req, user_id):
  user = get_object_or_404(models.UserProfile, pk=user_id)

  connection = get_object_or_404( 
    models.Connection,
    user_profile = req.user.get_profile(),
 	other_user_profile = user).delete()

  return redirect( user )

