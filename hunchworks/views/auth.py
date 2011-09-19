#!/usr/bin/env python

from hunchworks import forms
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as login_, logout
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.decorators import login_required


def _render(req, template, more_context):
  return render_to_response(
    "auth/" + template +".html",
    RequestContext(req, more_context))


def login(req):
  form = auth_forms.AuthenticationForm(
    data=(req.POST or None))

  if form.is_valid():
    login_(req, form.get_user())
    return redirect("home")

  return _render(req, "login", {
    "form": form
  })


def signup(req):
  form = auth_forms.UserCreationForm(req.POST or None)

  if form.is_valid():
    user = form.save()

    # can this ever fail?
    user = authenticate(
      username=form.cleaned_data['username'],
      password=form.cleaned_data['password1'])

    if user is not None and user.is_active:
      login_(req, user)
      return redirect("home")

  return _render(req, "signup", {
    "form": form
  })


def logout_view(req):
  logout(req)
  return redirect("index")


@login_required
def invitePeople(req):
  form = forms.InvitePeople(req.POST or None)
    
  if form.is_valid(): # All validation rules pass
    form.save(req.user.pk)
  print form.errors

  return redirect("profile")


def importFacebook(request):
  return render_to_response('importFacebook.html')


def importLinkedIn(request):
  return render_to_response('importLinkedIn.html', RequestContext(request))


def importTeamWorks(request):
  return render_to_response('importTeamWorks.html', RequestContext(request))