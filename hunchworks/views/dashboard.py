#!/usr/bin/env python
# encoding: utf-8

from hunchworks import models, hunchworks_enums
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


def _render(req, template, more_context):
  return render_to_response(
    "dashboard/" + template +".html",
    RequestContext(req, more_context))


@login_required
def dashboard(req):
  return _render(req, "home", {
    "events": req.user.get_profile().events()
  })
