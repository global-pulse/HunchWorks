#!/usr/bin/env python

from hunchworks import models, forms, hunchworks_enums
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
def open(req):
  """Render hunches with status = undetermined"""
  hunches_ = models.Hunch.objects.filter(
    privacy=hunchworks_enums.PrivacyLevel.OPEN, status=2
    ).order_by("-time_modified")
  hunches = paginated(req, hunches_, 10)
  return _render(req, "open", {
    "hunches": hunches
  })

@login_required
def finished(req):
  """Render hunches with status = ( denied or confirmed )"""
  hunches_ = models.Hunch.objects.filter(
    privacy=hunchworks_enums.PrivacyLevel.OPEN, status__in=(0,1)
    ).order_by("-time_modified")
  hunches = paginated(req, hunches_, 10)
  return _render(req, "finished", {
    "hunches": hunches
  })

@login_required
def show(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  comment_form = forms.HunchCommentForm(data=req.POST or None)

  if len(hunch.user_profiles.filter(pk=req.user.get_profile().pk)) > 0:
    following = True
  else:
    following = False

  if not hunch.is_viewable_by(req.user):
    raise PermissionDenied

  if comment_form.is_valid():
    comment = comment_form.save(commit=False)
    comment.creator = req.user.get_profile()
    comment.hunch = hunch
    comment.save()
    return redirect(comment)

  return _render(req, "show", {
    "following" : following,
    "hunch": hunch,
    "comment_form": comment_form
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


@login_required
def follow(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  hunch_user = models.HunchUser.objects.get_or_create(hunch=hunch, user_profile=req.user.get_profile())
  return redirect(index)


@login_required
def unfollow(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  hunch_user = get_object_or_404(models.HunchUser, hunch=hunch, user_profile=req.user.get_profile()).delete()
  return redirect(index)
