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
  groups = paginated(req, all_groups, 4)

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

  context = RequestContext(req)
  if req.method == "POST":
    form = forms.GroupForm(req.POST, instance=group)
    if form.is_valid():
      group = form.save()
      
      #create new collaborators for this group
      group_collaborators = req.POST['group_collaborators']
      group_collaborators = group_collaborators.split(',')
      group_collaborators.append( req.user.pk )
      for user_id in group_collaborators:
        group_connection = models.GroupConnection.objects.get_or_create(
          user=models.User.objects.get(pk=user_id),
          group=group,
          access_level=0,
          status=0)

      #remove unneeded collaborators from this hunch
      group_connections = models.GroupConnection.objects.filter(group=group_id)

      for group_connection in group_connections:
        if str(group_connection.user_id) not in group_collaborators:
          models.GroupConnection.objects.get(pk=group_connection.pk).delete()

      return redirect(group)
  else:
    form = forms.GroupForm(instance=group)

  context.update({ 'form':form, 'group':group,
    'user_id': req.user.pk })
  return _render(req, "edit", context)


@login_required
def create(req):
  context = RequestContext(req)

  if req.method == 'POST':
    form = forms.GroupForm(req.POST)
    
    if form.is_valid():
      hw_group = form.save()
      
      group_collaborators = req.POST['group_collaborators']
      group_collaborators = group_collaborators.split(',')
      group_collaborators.append( req.user.pk )
      for user_id in group_collaborators:
        group_connection = models.GroupConnection.objects.create(
          user=models.User.objects.get(pk=user_id),
          group=hw_group,
          access_level=0,
          status=0)

      return redirect(hw_group)
    else:
      form = forms.GroupForm(req.POST)
  else:
    form = forms.GroupForm()

  context.update({ 'form':form, 'user_id': req.user.pk })
  return _render(req, "create", context)
