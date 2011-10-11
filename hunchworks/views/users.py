#!/usr/bin/env python
# encoding: utf-8

import os
from hunchworks import models, forms
from django.conf import settings
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
def profile(req, user_id=None):
  if not user_id:
    user_id = req.user.get_profile().pk
  user_profile = get_object_or_404(models.UserProfile, pk=user_id)
  
  connected = None
  not_me = True
  if req.user.get_profile() == user_profile:
    not_me = False
  elif user_profile in req.user.get_profile().connections.all():
    connected = True
  else:
    connected = False

  #Get hunches that contain user's skill set
  hunches = models.Hunch.objects.filter(
    Q(skills__in=user_profile.skills.all()) |
    Q(languages__in=user_profile.languages.all())
    ).distinct()

  invite_form = forms.InvitePeople()
  context = RequestContext(req)
  context.update({ "user_profile": user_profile,
                   "invite_form": invite_form,
                   "hunches": hunches,
                   "connected": connected,
                   "not_me": not_me})
  return _render(req, "profile", context)

@login_required
def edit(req, user_id=None):
  if not user_id:
    user_id = req.user.pk
  user = get_object_or_404(models.User, pk=user_id)
  context = RequestContext(req)
  if req.method == 'POST': #If the form has been submitted
    form = forms.UserForm(req.POST, req.FILES, instance=user.get_profile())
    if form.is_valid():
      # do something with image here one day
      for file in req.FILES:
        handle_uploaded_file(req.FILES[file])
      update = form.save(commit=False)
      update.user = req.user
      update.save()
      context.update({ "user": user })
      return _render(req, "profile", context)
    else:
      context.update({ "user": user, "form": form })
      return _render(req, "edit", context) # Redirect after POST
  else:
    form = forms.UserForm(instance=user.get_profile())
    context.update({ "user": user, "form": form })
    return _render(req, "edit", context)

@login_required
def connections(req, user_id=None):
  if not user_id:
    user_id = req.user.pk
  user_profile = get_object_or_404(models.UserProfile, pk=user_id)
  connected_profiles = user_profile.connections.all()
  context = RequestContext(req)
  context.update({ "connected_profiles":connected_profiles})
  return _render(req, "connections", context)

def handle_uploaded_file(f):
  dest_path = settings.MEDIA_ROOT + '/profile_images/'
  if not os.path.exists(dest_path):
    os.makedirs(dest_path)
  destination = open(dest_path + str(f) , 'wb+')
  for chunk in f.chunks():
      destination.write(chunk)
  destination.close()
  
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

