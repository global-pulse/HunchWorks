#!/usr/bin/env python

from hunchworks import models, forms
from hunchworks.utils.pagination import paginated
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


def _render(req, template, more_context):
  return render_to_response(
    "hunches/" + template + ".html",
    RequestContext(req, more_context))


@login_required
def index(req):
  if( len(req.user.get_profile().hunch_set.all()) > 0):
    return redirect( my )
  else:
    return redirect( all )
  
@login_required
def my(req):
  hunches = paginated(req, req.user.get_profile().hunch_set.all(), 10)

  return _render(req, "my", {
    "hunches": hunches
  })
  
@login_required
def all(req):
  hunches = paginated(req, models.Hunch.objects.all(), 10)

  return _render(req, "all", {
    "hunches": hunches
  })


@login_required
def show(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)

  return _render(req, "show", {
    "hunch": hunch
  })


@login_required
def edit(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  form = forms.HunchForm(req.POST or None, instance=hunch)

  if form.is_valid():
    hunch = form.save()
    return redirect(hunch)

  return _render(req, "edit", {
    "hunch": hunch, "user": req.user,
    "form": form
  })


@login_required
def create(req):
  form = forms.HunchForm(req.POST or None)

  if form.is_valid():
    hunch = form.save(creator = req.user.get_profile())
    return redirect(hunch)

  return _render(req, "create", {
    "form": form, "user": req.user.get_profile()
  })


def showHunch(req, hunch_id):
  """Show a Hunch."""
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)

  if not hunch.is_viewable_by(req.user):
    raise PermissionDenied

  context = RequestContext(req)
  context.update({ "hunch": hunch })
  return render_to_response('showHunch.html', context)
