#!/usr/bin/env python
# encoding: utf-8

from hunchworks import models, forms
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def _render(req, template, more_context):
  return render_to_response(
    "users/" + template +".html",
    RequestContext(req, more_context))

@login_required
def profile(req, user_id=None):
  if not user_id:
    user_id = req.user.pk
  user = get_object_or_404(models.User, pk=user_id)

  #Get hunches that contain user's skill set
  hunches = models.Hunch.objects.filter(
    Q(skills__in=user.get_profile().skills.all()) |
    Q(languages__in=user.get_profile().languages.all())).distinct()

  invite_form = forms.InvitePeople()
  context = RequestContext(req)
  context.update({ "user": user,
                   "invite_form": invite_form,
                   "hunches": hunches})
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
      update = form.save(commit=False)
      update.user = models.UserProfile.objects.get(id = user_id)
      update.save()
      context.update({ "user": user })
      return _render(req, "profile", context)
    else:
      return _render(req, "edit", context) # Redirect after POST
  else:
    profile_form = forms.UserForm(instance=user.get_profile())
    context.update({ "user": user, "profile_form": profile_form })
    return _render(req, "edit", context)

@login_required
def connections(req, user_id=None):
  if not user_id:
    user_id = req.user.pk
  user = get_object_or_404(models.User, pk=user_id)
  context = RequestContext(req)
  return _render(req, "profile", context)
