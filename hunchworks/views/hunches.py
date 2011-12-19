#!/usr/bin/env python

from django.db import transaction
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.core.files.storage import get_storage_class
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from formwizard.views import SessionWizardView
from hunchworks import models, forms, hunchworks_enums
from hunchworks.utils.pagination import paginated


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
    privacy=hunchworks_enums.PrivacyLevel.OPEN,
    ).order_by("-time_modified")
  hunches = paginated(req, hunches_, 10)
  return _render(req, "open", {
    "hunches": hunches
  })

@login_required
def finished(req):
  """Render hunches with status = ( denied or confirmed )"""
  hunches_ = models.Hunch.objects.filter(
    privacy=hunchworks_enums.PrivacyLevel.OPEN,
    ).order_by("-time_modified")
  hunches = paginated(req, hunches_, 10)
  return _render(req, "finished", {
    "hunches": hunches
  })


@login_required
def show(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)


  hunch_evidence_form = None
  invite_form = None
  invited = None

  if req.method == "POST":
    action = req.POST.get("action")

    if action == "add_evidence":
      hunch_evidence_form = forms.HunchEvidenceForm(req.POST)

      if hunch_evidence_form.is_valid():
        hunch_evidence = hunch_evidence_form.save(creator=req.user.get_profile())
        return redirect(hunch_evidence)

    elif action == "invite":
      invite_form = forms.InviteForm(req.POST)

      if invite_form.is_valid():

        # send the intivtes and clear the form, so it's reinstantiated later.
        invited = invite_form.send_invites(inviter=req.user.get_profile())
        invite_form = None

  if hunch_evidence_form is None:
    hunch_evidence_form = forms.HunchEvidenceForm(initial={
      "hunch": hunch
    })

  if invite_form is None:
    invite_form = forms.InviteForm(initial={
      "hunch": hunch
    })


  if len(hunch.user_profiles.filter(pk=req.user.get_profile().pk)) > 0:
    following = True
  else:
    following = False


  return _render(req, "show/summary", {
    "hunch": hunch,
    "add_hunch_evidence_form": hunch_evidence_form,
    "invite_form": invite_form,
    "invited": invited,
    "following": following
  })


@login_required
def activity(req, hunch_id):
  hunch = get_object_or_404(
    models.Hunch,
    pk=hunch_id)

  events = paginated(req, hunch.events(), 20)

  return _render(req, "show/activity", {
    "hunch": hunch,
    "events": events
  })


@login_required
def evidence(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  hunch_evidences = paginated(req, models.HunchEvidence.objects.filter(hunch=hunch), 20)

  return _render(req, "show/evidence", {
    "hunch": hunch,
    "hunch_evidences": hunch_evidences,
  })


@login_required
def comments(req, hunch_id):
  hunch = get_object_or_404(
    models.Hunch,
    pk=hunch_id)

  form = forms.CommentForm(req.POST or None, initial={
    "hunch": hunch
  })

  if form.is_valid():
    comment = form.save(creator=req.user.get_profile())
    return redirect(comment)

  return _render(req, "show/comments", {
    "hunch": hunch,
    "comments": hunch.comment_set.all(),
    "form": form
  })


@login_required
def contributors(req, hunch_id):
  hunch = get_object_or_404(
    models.Hunch,
    pk=hunch_id)

  form = None

  if req.method == "POST":
    form = forms.InviteForm(req.POST)
    if form.is_valid():
    
      # Send the invitations and clear the form. If the form wasn't valid,
      # the form with errors will be shown again for correcting.
      form.send_invites(inviter=req.user.get_profile())
      form = None

  if form is None:
    form = forms.InviteForm(initial={
      "hunch": hunch
    })

  return _render(req, "show/contributors", {
    "contributors": hunch.contributors,
    "hunch": hunch,
    "form": form
  })


@login_required
def edit(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  form = forms.HunchEditForm(req.POST or None, instance=hunch)

  if form.is_valid():
    hunch = form.save()
    return redirect(hunch)

  return _render(req, "edit", {
    "hunch": hunch,
    "form": form
  })


@login_required
def permissions(req, hunch_id):
  hunch = get_object_or_404(
    models.Hunch,
    pk=hunch_id)

  form = forms.HunchPermissionsForm(
    req.POST or None,
    instance=hunch)

  if form.is_valid():
    hunch = form.save()
    return redirect(hunch)

  return _render(req, "permissions", {
    "hunch": hunch,
    "form": form
  })


class HunchWizard(SessionWizardView):
  file_storage = get_storage_class()
  def get_template_names(self):
    return "hunches/create/%s.html" %\
      self.steps.step1

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
      return super(HunchWizard, self)\
        .dispatch(*args, **kwargs)

  def done(self, form_list, **kwargs):
    with transaction.commit_on_success():

      hunch = models.Hunch.objects.create(
        creator     = self.request.user.get_profile(),
        title       = form_list[0].cleaned_data["title"],
        description = form_list[0].cleaned_data["description"],
        privacy     = form_list[0].cleaned_data["privacy"],
        location    = form_list[2].cleaned_data["location"])

      hunch.tags = form_list[2].cleaned_data["tags"]
      hunch.user_profiles = form_list[3].cleaned_data["user_profiles"]

      for evidence in form_list[1].cleaned_data["evidences"]:
        models.HunchEvidence.objects.create(
          creator=self.request.user.get_profile(),
          evidence=evidence,
          hunch=hunch)

      hunch.save()

    return redirect(hunch)


@login_required
def follow(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  hunch.userprofile_set.add(req.user.get_profile())
  return redirect(index)


@login_required
def unfollow(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  hunch.userprofile_set.remove(req.user.get_profile())
  return redirect(index)


@login_required
def add_evidence(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)

  if req.method == "POST":
    form = forms.HunchEvidenceForm(req.POST)

    if form.is_valid():
      hunch_evidence = form.save(creator=req.user.get_profile())
      return redirect(hunch)

  else:
    form = forms.HunchEvidenceForm(initial={
      "hunch": hunch
    })

  return _render(req, "show/add_evidence", {
    "hunch": hunch,
    "form": form
  })
