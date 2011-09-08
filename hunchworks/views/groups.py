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
  all_groups = models.HwGroup.objects.all()
  groups = paginated(req, all_groups, 4)

  return _render(req, "index", {
    "groups": groups
  })


@login_required
def show(req, group_id):
  group = get_object_or_404(models.HwGroup, pk=group_id)

  return _render(req, "show", {
    "group": group
  })


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

  return _render(req, "edit", {
    "group": group,
    "form": form
  })


@login_required
def new(req):
  if req.method == "POST":
    form = forms.GroupForm(req.POST)
    if form.is_valid():
      group = form.save()
      return redirect(group)
  else:
    form = forms.GroupForm()

  return _render(req, "new", {
    "form": form
  })


def createGroup(request):
  context = RequestContext(request)

  if request.method == 'POST':
    hw_group_form = forms.HwGroupForm(request.POST)
    
    if hw_group_form.is_valid():
      hw_group = hw_group_form.save()
      
      group_collaborators = request.POST['group_collaborators']
      group_collaborators = group_collaborators.split(',')
      group_collaborators.append( request.user.pk )
      for user_id in group_collaborators:
        group_connection = models.HwGroupConnections.objects.create(
          user=models.HwUser.objects.get(pk=user_id),
          group=hw_group,
          access_level=0,
          status=0)

      return HttpResponseRedirect('/hunchworks/profile')
    else:
      group_form = forms.HwGroupForm(request.POST)
  else:
    group_form = forms.HwGroupForm()

  context.update({ 'group_form':group_form,
    'user_id': request.user.pk })
  return render_to_response('createGroup.html', context)
