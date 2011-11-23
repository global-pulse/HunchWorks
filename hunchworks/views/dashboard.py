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
  p = req.user.get_profile()
  return _render(req, "home", {
    "events":    paginated(req, p.events(),           20),
    "hunches":   paginated(req, p.hunch_set.all(),    10),
    "bookmarks": paginated(req, p.bookmark_set.all(), 10)
  })
