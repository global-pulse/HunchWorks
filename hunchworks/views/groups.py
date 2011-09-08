#!/usr/bin/env python
# encoding: utf-8

from hunchworks import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def createGroup(request):
  form = forms.CreateGroupForm()
  context = RequestContext(request)
  context['form'] = form;
  return render_to_response('createGroup.html', context)