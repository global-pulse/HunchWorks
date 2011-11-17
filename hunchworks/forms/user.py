#!/usr/bin/env python

from django import forms
from hunchworks import models


class UserForm(forms.ModelForm):
  class Meta:
    model= models.UserProfile
    exclude = ("user", "roles", "qualifications", "courses", "location_interests")
