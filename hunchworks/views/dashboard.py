#!/usr/bin/env python
# encoding: utf-8

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from hunchworks.utils.pagination import paginated
from hunchworks import models, hunchworks_enums


def _render(req, template, more_context):
  return render_to_response(
    "dashboard/" + template +".html",
    RequestContext(req, more_context))


@login_required
def dashboard(req):
  events = paginated(req, req.user.get_profile().events(), 20)
  hunches = paginated(req, req.user.get_profile().hunch_set.all(), 10)

  return _render(req, "home", {
    "events": events,
    "hunches": hunches
  })
