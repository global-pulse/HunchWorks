#!/usr/bin/env python

from hunchworks import forms
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login as login_, logout
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.decorators import login_required


def login(request):
  if request.method == "POST":

    # We must use a named arg here, since AuthenticationForm expects the
    # first arg to be an HttpRequest (to check if cookies are enabled).
    form = auth_forms.AuthenticationForm(
      data=request.POST)

    if form.is_valid():
      user = authenticate(
        username=request.POST['username'],
        password=request.POST['password'])

      if user is not None and user.is_active:
          login_(request, user)
          return HttpResponseRedirect(
            reverse("home"))

  else:
    form = auth_forms.AuthenticationForm()

  return render_to_response("login.html", {
    "form": form
  }, context_instance=RequestContext(request))


def logout_view(request):
  logout(request)
  return render_to_response('index.html')


@transaction.commit_on_success
def signup(request):
  context = RequestContext(request)

  if request.method == "POST":
    data = request.POST.copy()
    data.update({'is_active':1, 'is_staff':0, 'is_superuser':0,
              'last_login':datetime.datetime.today(),
              'date_joined':datetime.datetime.today(),
              })
    auth_user_form = forms.AuthUserForm(data, instance=models.User())
    hw_user_form = forms.UserForm(data, instance=models.User())

    if auth_user_form.is_valid() and hw_user_form.is_valid():
      user = auth_user_form.save()
      user.set_password(request.POST['password'])
      user.save()
      #if not user.save():
      #  raise DatabaseError
      hw_user = hw_user_form.save(commit=False)
      hw_user.user_id = user
      hw_user.save()
      #if not hw_user.save():
      #  raise DatabaseError

      languages = request.POST['languages']
      languages = languages.split(',')
      for skill_id in languages:
        skill_connection = models.SkillConnection.objects.create(
          skill=models.Skill.objects.get(pk=skill_id),
          user=models.User.objects.get(pk=user.pk),
          level=1)

      skills = request.POST['skills']
      skills = skills.split(',')
      for skill_id in skills:
        skill_connection = models.SkillConnection.objects.create(
          skill=models.Skill.objects.get(pk=skill_id),
          user=models.User.objects.get(pk=user.pk),
          level=1)

      try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
          if user.is_active:
            login_(request, user)
            return HttpResponseRedirect( reverse(home ))
      except exceptions.ObjectDoesNotExist:
        pass
        #TODO(Chris:2011-8-24) Find something to do with thrown exception

    else:
      auth_user_form = forms.AuthUserForm(request.POST)
      hw_user_form = forms.UserForm(request.POST)

  else:
    auth_user_form = forms.AuthUserForm()
    hw_user_form = forms.UserForm()

  context['auth_user_form'] = auth_user_form
  context['hw_user_form'] = hw_user_form
  return render_to_response("signup.html", context)


@login_required
def invitePeople(request):
  if request.method == 'POST': # If the form has been submitted...
    form = forms.InvitePeople(request.POST)
    if form.is_valid(): # All validation rules pass
      form.save()
    else:
      return HttpResponseRedirect('profile.html') # Redirect after POST
  return render_to_response('profile.html', RequestContext(request))


def importFacebook(request):
  return render_to_response('importFacebook.html')


def importLinkedIn(request):
  return render_to_response('importLinkedIn.html', RequestContext(request))


def importTeamWorks(request):
  return render_to_response('importTeamWorks.html', RequestContext(request))