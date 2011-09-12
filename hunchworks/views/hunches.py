#!/usr/bin/env python

from hunchworks import models, forms
from hunchworks.utils.pagination import paginated
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


def _render(req, template, more_context):
  return render_to_response(
    "hunches/" + template + ".html",
    RequestContext(req, more_context))


@login_required
def index(req):
  all_hunches = models.Hunch.objects.all()
  hunches = paginated(req, all_hunches, 4)

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
    hunch = form.save()
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


@login_required
def createHunch(request):
  """Create a Hunch.  Assumes Hunch.user = request.user! """
  context = RequestContext(request)
  if request.method == 'POST':

    data = request.POST.copy()
    data.update({'creator':request.user.pk, 'status':2})
    hw_hunch_form = forms.HunchForm(data, instance=models.Hunch())
    hw_evidence_form = forms.EvidenceForm(data, instance=models.Evidence())

    if hw_hunch_form.is_valid() and hw_evidence_form.is_valid():
      hw_hunch = hw_hunch_form.save()

      languages_required = request.POST['languages_required']
      languages_required = languages_required.split(',')
      for skill_id in languages_required:
        skill_connection = models.SkillConnection.objects.create(
          skill=models.Skill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)

      skills_required = request.POST['skills_required']
      skills_required = skills_required.split(',')
      for skill_id in skills_required:
        skill_connection = models.SkillConnection.objects.create(
          skill=models.Skill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)

      tags = request.POST['tags']
      tags = tags.split(',')
      for tag_id in tags:
        tag_connection = models.TagConnection.objects.create(
          tag=models.Tag.objects.get(pk=tag_id),
          hunch=hw_hunch)

      hunch_collaborators = request.POST['hunch_collaborators']
      hunch_collaborators = hunch_collaborators.split(',')
      hunch_collaborators.append( request.user.pk )
      for user_id in hunch_collaborators:
        hunch_connection = models.HunchConnection.objects.create(
          user=models.User.objects.get(pk=user_id),
          hunch=hw_hunch,
          status=0)

      hw_evidence = hw_evidence_form.save(commit=False)
      hw_evidence.hunch_id = hw_hunch.pk
      hw_evidence.save()
      return HttpResponseRedirect('/hunchworks/profile')
    else:
      hunch_form = forms.HunchForm(request.POST)
      evidence_form = forms.EvidenceForm(request.POST)
  else:
    hunch_form = forms.HunchForm()
    evidence_form = forms.EvidenceForm()

  context.update({ 'hunch_form':hunch_form, 'evidence_form':evidence_form,
    'user_id': request.user.pk })
  return render_to_response('createHunch.html', context)


@login_required
def editHunch(request, hunch_id):
  """Edit a Hunch."""
  hunch = get_object_or_404(models.Hunch, pk=hunch_id)
  if not hunch.is_editable_by(request.user):
    raise PermissionDenied

  context = RequestContext(request)
  if request.method == 'POST':
    data = request.POST.copy()
    data.update({'creator':request.user.pk, 'status':2})
    hw_hunch_form = forms.HunchForm(data, instance = hunch)

    if hw_hunch_form.is_valid():
      hw_hunch = hw_hunch_form.save()

      #create new language skills for this hunch
      languages_required = request.POST['languages_required']
      languages_required = languages_required.split(',')
      for skill_id in languages_required:
        skill_connection = models.SkillConnection.objects.get_or_create(
          skill=models.Skill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)

    #create new non language skills for this hunch
      skills_required = request.POST['skills_required']
      skills_required = skills_required.split(',')
      for skill_id in skills_required:
        skill_connection = models.SkillConnection.objects.get_or_create(
          skill=models.Skill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)

      #remove unneeded language and skills from this hunch
      skill_connections = models.SkillConnection.objects.filter(hunch=hunch_id)
      skills = languages_required + skills_required

      for skill_connection in skill_connections:
        if str(skill_connection.skill_id) not in skills:
          models.SkillConnection.objects.get(pk=skill_connection.pk).delete()

      #create new tags for this hunch
      tags = request.POST['tags']
      tags = tags.split(',')
      for tag_id in tags:
        tag_connection = models.TagConnection.objects.get_or_create(
          tag=models.Tag.objects.get(pk=tag_id),
          hunch=hw_hunch)

      #remove unneeded tags from this hunch
      tag_connections = models.TagConnection.objects.filter(hunch=hunch_id)

      for tag_connection in tag_connections:
        if str(tag_connection.tag_id) not in tags:
          models.TagConnection.objects.get(pk=tag_connection.pk).delete()

      #create new collaborators for this hunch
      hunch_collaborators = request.POST['hunch_collaborators']
      hunch_collaborators = hunch_collaborators.split(',')
      hunch_collaborators.append( request.user.pk )
      for user_id in hunch_collaborators:
        hunch_connection = models.HunchConnection.objects.get_or_create(
          user=models.User.objects.get(pk=user_id),
          hunch=hw_hunch,
          status=0)

      #remove unneeded collaborators from this hunch
      hunch_connections = models.HunchConnection.objects.filter(hunch=hunch_id)

      for hunch_connection in hunch_connections:
        if str(hunch_connection.user_id) not in hunch_collaborators:
          models.HunchConnection.objects.get(pk=hunch_connection.pk).delete()

      return HttpResponseRedirect('/hunchworks/profile')
    else:
      hunch_form = forms.HunchForm(request.POST)
  else:
    hunch_form = forms.HunchForm(instance = hunch)

  context.update({ 'hunch_id': hunch_id, 'user_id': request.user.pk,
    'hunch_form': hunch_form })
  return render_to_response('editHunch.html', context)