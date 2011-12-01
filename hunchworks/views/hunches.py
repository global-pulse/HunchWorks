#!/usr/bin/env python

from django.db import transaction
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
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
  hunch = get_object_or_404(
    models.Hunch,
    pk=hunch_id)

  # This is kind of nuts. It's a work-around to Python's lexical scope rules.
  # The _id_counter var can't be a simple int, since those are immutable, and
  # rebinding it within _auto_id (as in: _id_counter +=1) would prevent us from
  # accessing the var in the outer scope.

  _id_counter = [0]
  def _auto_id():
    _id_counter[0] += 1
    return ("form_%s_id_" % _id_counter[0]) + "%s"

  # If one of the HunchEvidence comment forms was just submitted, attempt the
  # usual validate -> save -> redirect process. If this fails (i.e. the form was
  # not valid), we'll need it later on to display again.

  comment_form = None
  vote_form = None

  if req.method == "POST":
    action = req.POST.get("action")

    if action == "comment":
      comment_form = forms.CommentForm(req.POST, auto_id=_auto_id())

      if comment_form.is_valid():
        comment = comment_form.save(creator=req.user.get_profile())
        return redirect(comment)

    elif action == "vote":
      vote_form = forms.VoteForm(req.POST, auto_id=_auto_id())

      if vote_form.is_valid():
        vote = vote_form.save(user_profile=req.user.get_profile())
        return redirect(vote_form.cleaned_data["hunch_evidence"])

  def _wrap(hunch_evidence):
    """
    For a given ``hunch_evidence``, return a tuple containing:

      * The HunchEvidence object itself.
      * A QuerySet of the related comments.
      * A CommentForm for creating new comments related to the HunchEvidence.
      * A VoteForm for creating or changing a vote related to the HunchEvidence.
    """

    he_pk = unicode(hunch_evidence.pk)

    def _submitted(form):
      if form is not None:
        if he_pk == unicode(form["hunch_evidence"].value()):
          return True

    # If a comment form was just submitted for this HE, use it.
    if _submitted(comment_form):
      cf = comment_form

    else:
      cf = forms.CommentForm(initial={
        "hunch_evidence": hunch_evidence
      }, auto_id=_auto_id())

    # If a vote form was just submitted for this HE, use it.
    if _submitted(vote_form):
      vf = vote_form

    # If the user has already voted on this HE, show an edit form. Otherwise,
    # show a create form.
    else:
      try:
        vf = forms.VoteForm(instance=models.Vote.objects.get(
          hunch_evidence=hunch_evidence,
          user_profile=req.user.get_profile()
        ), auto_id=_auto_id())

      except models.Vote.DoesNotExist:
        vf = forms.VoteForm(initial={
          "hunch_evidence": hunch_evidence
        }, auto_id=_auto_id())

    return (hunch_evidence, hunch_evidence.comment_set.all(), cf, vf)



  return _render(req, "show/evidence", {
    "hunch": hunch,
    "evidences_for": map(_wrap, hunch.evidences_for()),
    "evidences_against": map(_wrap, hunch.evidences_against()),
  })


@login_required
def comments(req, hunch_id):
  hunch = get_object_or_404(
    models.Hunch,
    pk=hunch_id)

  return _render(req, "show/comments", {
    "hunch": hunch
  })


@login_required
def contributors(req, hunch_id):
  hunch = get_object_or_404(
    models.Hunch,
    pk=hunch_id)

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


def add_evidence(req, hunch_id):
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)

  if req.method == "POST":
    form = forms.HunchEvidenceForm(req.POST)

    if form.is_valid():
      hunch_evidence = form.save(user_profile=req.user.get_profile())
      return redirect(hunch)

  else:
    form = forms.HunchEvidenceForm(initial={
      "hunch": hunch
    })

  return _render(req, "show/add_evidence", {
    "hunch": hunch,
    "form": form
  })