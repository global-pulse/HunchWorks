#!/usr/bin/env python
# encoding: utf-8

from hunchworks import models, hunchworks_enums
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


def index(request):
  return render_to_response('index.html')

@login_required
def home(request):
  user_id = request.user.pk
  recent_hunches = models.HwHunch.objects.filter(privacy=hunchworks_enums.PrivacyLevel.OPEN).order_by("-time_modified")[:5]
  context = RequestContext(request)
  context.update({'recent_hunches': recent_hunches })
  return render_to_response('home.html', context)