#!/usr/bin/env python
# encoding: utf-8

from hunchworks import models, hunchworks_enums
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(req):
  recent_hunches = \
          models.Hunch.objects.filter(
            privacy=hunchworks_enums.PrivacyLevel.OPEN, status=2
            ).order_by("-time_modified")[:5]
  confirmed_hunches = \
          models.Hunch.objects.filter(
                  privacy=hunchworks_enums.PrivacyLevel.OPEN, status__in=(0,1)
                  ).order_by("-time_modified")[:5]
  suggested_groups = models.Group.objects.exclude(pk__in=req.user.get_profile().group_set.all())
  suggested_people = models.UserProfile.objects.exclude(pk__in=req.user.get_profile().connections.all()).exclude(pk=req.user.get_profile().pk)
  context = RequestContext(req)
  context.update({'recent_hunches': recent_hunches,
      'confirmed_hunches': confirmed_hunches,
      'suggested_groups': suggested_groups,
      'suggested_people': suggested_people })
  return render_to_response('dashboard/home.html', context)

@login_required
def connect(req, user_id):
  user = get_object_or_404(models.UserProfile, pk=user_id)

  connection = models.Connection.objects.get_or_create(
    user_profile = models.UserProfile.objects.get(pk=req.user.get_profile().pk),
	other_user_profile = models.UserProfile.objects.get(pk=user_id),
	status=0)
  
  return redirect( user )
