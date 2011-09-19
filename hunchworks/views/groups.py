#!/usr/bin/env python
# encoding: utf-8

from hunchworks import forms, models
from hunchworks.utils.pagination import paginated
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


def _render(req, template, more_context):
  return render_to_response(
    "groups/" + template +".html",
    RequestContext(req, more_context))


@login_required
def index(req):
  all_groups = models.Group.objects.all()
  groups = paginated(req, all_groups, 20)

  return _render(req, "index", {
    "groups": groups
  })


@login_required
def show(req, group_id):
  group = get_object_or_404(models.Group, pk=group_id)

  return _render(req, "show", {
    "group": group
  })


@login_required
def edit(req, group_id):
  group = get_object_or_404(models.Group, pk=group_id)
  form = forms.GroupForm(req.POST or None, instance=group)

  if form.is_valid():
    group = form.save()
    return redirect(group)

  return _render(req, "edit", { 'form':form, 'group':group,
    'user_id': req.user.pk })

@login_required
def join(req, group_id):
  group = get_object_or_404(models.Group, pk=group_id)

  group_connection = models.UserProfileGroup.objects.get_or_create(
    user_profile = models.UserProfile.objects.get(pk=req.user.pk),
	group = group,
	status=0)

  return _render(req, "show", { 'group': group })

@login_required
def create(req):
  form = forms.GroupForm(req.POST or None)
    
  if form.is_valid():
    group = form.save()
    return redirect(group)

  return _render(req, "create", { 'form':form, 'user_id': req.user.pk })
