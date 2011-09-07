#!/usr/bin/env python
# Forms used in the project
# Author: Auto created by Texas
# Date: 2011-06-20
# License:  This  program  is  free  software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the  Free Software Foundation; either version 3 of the License, or (at your
# option)  any later version. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.

import models
import custom_fields

from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput


class LoginForm(forms.Form):
  username = forms.CharField( max_length=30 )
  password = forms.CharField( max_length=30, widget=forms.PasswordInput() )


class AuthUserForm(ModelForm):

  class Meta:
    model= models.User
    exclude = ( 
    'groups', 'user_permissions',
    )
    widgets = {
      'password': PasswordInput()
      }

class HwUserForm(ModelForm):
  skill_name = forms.CharField( max_length=100 )

  class Meta:
    model = models.HwUser
    exclude = (
    'show_profile_reminder', 'bio_text', 'phone', 'skills', 'user_id',
	'skype_name', 'website', 'profile_picture', 'education', 'classes', 
	'location_interests', 'roles', 'hunches', 'invited_users', 'groups',
	'collaborators', 'user',
	)

class HwHunchForm(ModelForm):
  skills_required = forms.CharField()
  languages_required = forms.CharField()
  tags_required = forms.CharField()
  hunch_collaborators = forms.CharField()

  class Meta:
    model = models.HwHunch
    exclude = (
    'hunch_id', 'skills', 'groups', 'users', 'invited_users', 'tags',
    'time_created', 'time_modified', 'hunch_strength',
    )
    
class HwEvidenceForm(ModelForm):
    
  class Meta:
    model = models.HwEvidence
    exclude = (
    'hunch_id', 'creator_id', 'evidence_strength', 'time_created',
    'time_modified', 'attachments', 'albums', 'hunch', 'tags'
    )

class CreateGroupForm(ModelForm):
  logo = forms.CharField( max_length=100)

  class Meta:
    model= models.HwGroup
    exclude = ( 'logo' )


class HomepageForm(ModelForm):
  class Meta:
    model = models.HwUser


class InvitePeople(forms.Form):
  invited_emails = custom_fields.MultiEmailField(widget=forms.Textarea(
    attrs={'cols': 30, 'rows': 10}))
  
  def save(self, *args, **kwargs):
    created_user = models.HwUser.objects.get(pk=1)
    print self.cleaned_data
    #TODO( Chris: 8-15-2011): figure out how ot introspect invited_emails object instead
    # of using email_input
    for email_input in self.cleaned_data['invited_emails']:
      invited_email = models.HwInvitedUser( email=email_input )
      invited_user = models.HwUserInvites( invited_email=invited_email, user=created_user, status=0)
      invited_user.save()
    
