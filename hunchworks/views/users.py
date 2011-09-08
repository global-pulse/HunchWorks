#!/usr/bin/env python
# encoding: utf-8

from hunchworks import models, forms
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def profile(request, user_id=None):
  if not user_id:
    user_id = request.user.pk
  user = get_object_or_404(models.User, pk=user_id)
  invite_form = forms.InvitePeople()
  context = RequestContext(request)
  context.update({ "user": user, "invite_form": invite_form })
  return render_to_response('profile.html', context)
