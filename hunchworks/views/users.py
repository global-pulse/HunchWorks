#!/usr/bin/env python
# encoding: utf-8

from hunchworks import models, forms
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def profile(request, user_id=None):
  if not user_id:
    user_id = request.user.pk
  user = get_object_or_404(models.User, pk=user_id)
  invite_form = forms.InvitePeople()
  context = RequestContext(request)
  context.update({ "user": user, "invite_form": invite_form })
  return render_to_response('users/profile.html', context)

@login_required
def edit(request, user_id=None):
  if not user_id:
    user_id = request.user.pk
  user = get_object_or_404(models.User, pk=user_id)
  context = RequestContext(request)
  if request.method == 'POST': #If the form has been submitted
    form = forms.UserForm(request.POST)
    if form.is_valid():
      form.save()
      context.update({ "user": user })
      return render_to_response('/users/profile.html', context)
    else:
      return HttpResponseRedirect('/hunchworks/profile/edit') # Redirect after POST
  else:
    profile_form = forms.UserForm()
    context.update({ "user": user, "profile_form": profile_form })
    return render_to_response('users/edit.html', context)
