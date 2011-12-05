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

  invite_form = forms.InviteForm()
  context = RequestContext(req)
  context.update({ "user_profile": user_profile,
                   "invite_form": invite_form,
                   "hunches": [],
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
      for file in req.FILES:
        handle_uploaded_file(req.FILES[file], '/profile_images/')
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

