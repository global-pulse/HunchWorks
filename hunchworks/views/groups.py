#!/usr/bin/env python
# encoding: utf-8

from hunchworks import models, forms
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def createGroup(request):
  context = RequestContext(request)

  if request.method == 'POST':
    hw_group_form = forms.HwGroupForm(request.POST)
    
    if hw_group_form.is_valid():
      hw_group = hw_group_form.save()
      
      group_collaborators = request.POST['group_collaborators']
      group_collaborators = group_collaborators.split(',')
      group_collaborators.append( request.user.pk )
      for user_id in group_collaborators:
        group_connection = models.HwGroupConnections.objects.create(
          user=models.HwUser.objects.get(pk=user_id),
          group=hw_group,
          access_level=0,
          status=0)

      return HttpResponseRedirect('/hunchworks/profile')
    else:
      group_form = forms.HwGroupForm(request.POST)
  else:
    group_form = forms.HwGroupForm()

  context.update({ 'group_form':group_form,
    'user_id': request.user.pk })
  return render_to_response('createGroup.html', context)