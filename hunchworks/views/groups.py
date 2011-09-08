#!/usr/bin/env python
# encoding: utf-8

from hunchworks import forms, models
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

PER_PAGE = 20


@login_required
def index(req):
  all_groups = models.HwGroup.objects.all()
  paginator = Paginator(all_groups, PER_PAGE)

  try:
    page = int(req.GET.get("page", "1"))
  except ValueError:
    page = 1

  try:
    groups = paginator.page(page)
  except (EmptyPage, InvalidPage):
    groups = paginator.page(paginator.num_pages)

  return render_to_response("groups/index.html", RequestContext(req, {
    "groups": groups
  }))


@login_required
def show(req, group_id):
  group = get_object_or_404(models.HwGroup, pk=group_id)

  return render_to_response("groups/show.html", RequestContext(req, {
    "group": group
  }))


@login_required
def edit(req, group_id):
  group = get_object_or_404(models.HwGroup, pk=group_id)

  if req.method == "POST":
    form = forms.GroupForm(req.POST, instance=group)
    if form.is_valid():
      group = form.save()
      return redirect(group)
  else:
    form = forms.GroupForm(instance=group)

  return render_to_response("groups/edit.html", RequestContext(req, {
    "group": group,
    "form": form
  }))


@login_required
def new(req):
  if req.method == "POST":
    form = forms.GroupForm(req.POST)
    if form.is_valid():
      group = form.save()
      return redirect(group)
  else:
    form = forms.GroupForm()

  return render_to_response("groups/new.html", RequestContext(req, {
    "form": form
  }))
