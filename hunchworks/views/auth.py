#!/usr/bin/env python

from hunchworks import forms
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def _render(req, template, more_context):
  return render_to_response(
    "auth/" + template +".html",
    RequestContext(req, more_context))


def login(req):
  form = auth.forms.AuthenticationForm(
    data=(req.POST or None))

  if form.is_valid():
    auth.login(req, form.get_user())
    return redirect("dashboard")

  return _render(req, "login", {
    "form": form
  })


def signup(req):
  form = auth.forms.UserCreationForm(
    data=(req.POST or None))

  if form.is_valid():
    user = form.save()

    # can this ever fail?
    user = auth.authenticate(
      username=form.cleaned_data['username'],
      password=form.cleaned_data['password1'])

    if user is not None and user.is_active:
      auth.login(req, user)
      return redirect("dashboard")

  return _render(req, "signup", {
    "form": form
  })


def logout(req):
  auth.logout(req)
  return redirect("login")


@login_required
def invitePeople(req):
  form = forms.InvitePeople(req.POST or None)
    
  if form.is_valid(): # All validation rules pass
    form.save(req.user.pk)

  return redirect("profile")
