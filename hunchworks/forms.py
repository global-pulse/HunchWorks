#!/usr/bin/python2.7
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

from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput 

class LoginForm(ModelForm):
  class Meta:
    model= models.HwUser
    fields = ( 'username', 'password' )
    widgets = {
      'password': PasswordInput()
      }


class SignUpForm(ModelForm):
  skill_name = forms.CharField( max_length=100 )

  class Meta:
    model= models.HwUser
    exclude = ( 
	'show_profile_reminder', 'bio_text', 'phone', 'skills', 'user_id',
	'skype_name', 'website', 'profile_picture', 'education', 'classes', 
	'location_interests', 'roles', 'hunches', 'invited_users', 'groups'
	)
    widgets = {
      'password': PasswordInput()
      }


class CreateHunchForm(ModelForm):
  #tags = forms.CharField(max_length=40)
  #import datetime
  #time_created = forms.DateTimeField(initial=datetime.datetime.today)
  #creator_id = models.HwUser.objects.get(pk=1)
  #creator = models.HwUser.objects.get(pk=1)

  class Meta:
    model = models.HwHunch
    exclude = (
    'hunch_id', 'language', 'location', 'skills', 'groups', 'users',
    'invited_users', 'tags'
    )


class CreateGroup(ModelForm):
  logo = forms.CharField( max_length=100)

  class Meta:
    model= models.HwGroup


class HomepageForm(ModelForm):
  class Meta:
    model = models.HwUser


class InvitePeople(ModelForm):
  invited_emails = forms.CharField(widget=forms.Textarea(
    attrs={'cols': 30, 'rows': 10}))
  
  class Meta:
    model = models.HwInvitedUser
    fields = ()
