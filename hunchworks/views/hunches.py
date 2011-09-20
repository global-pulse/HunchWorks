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
  all_hunches = models.Hunch.objects.all()
  hunches = paginated(req, all_hunches, 10)

  return _render(req, "index", {
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
    hunch = form.save(commit=False)
    
    hunch.tags = req.POST["tags"].split(",")
    hunch.skills = req.POST["skills"].split(",")
    hunch.languages = req.POST["languages"].split(",")
    
    #create new collaborators for this hunch
    hunch_collaborators = req.POST["user_profiles"] + "," + str(req.user.pk)
    hunch_collaborators = hunch_collaborators.split(",")
    for user_id in hunch_collaborators:
      hunch_user = models.HunchUser.objects.get_or_create(
        user_profile=models.UserProfile.objects.get(pk=user_id),
        hunch=hunch,
        status=0)

    #remove unneeded collaborators from this hunch
    hunch_users = models.HunchUser.objects.filter(hunch=hunch_id)

    for hunch_user in hunch_users:
      if str(hunch_user.user_profile_id) not in hunch_collaborators:
        models.HunchUser.objects.get(pk=hunch_user.pk).delete()

    hunch.save()
    return redirect(hunch)

  return _render(req, "edit", {
    "hunch": hunch,
    "form": form
  })


@login_required
def create(req):
  form = forms.HunchForm(req.POST or None)

  if form.is_valid():
    hunch = form.save(commit=False)
    hunch.creator = req.user.get_profile()
    hunch.save()

    hunch.tags = req.POST["tags"].split(",")
    hunch.skills = req.POST["skills"].split(",")
    hunch.languages = req.POST["languages"].split(",")

    hunch_collaborators = req.POST["user_profiles"] + "," + str(req.user.pk)
    hunch_collaborators = hunch_collaborators.split(",")
    for user_id in hunch_collaborators:
      hunch_user = models.HunchUser.objects.create(
        user_profile=models.UserProfile.objects.get(pk=user_id),
        hunch=hunch,
        status=0)

    return redirect(hunch)

  return _render(req, "create", {
    "form": form
  })


def showHunch(request, hunch_id):
  """Show a Hunch."""
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)

  if not hunch.is_viewable_by(request.user):
    raise PermissionDenied

  context = RequestContext(request)
  context.update({ "hunch": hunch })
  return render_to_response('showHunch.html', context)
