#!/usr/bin/env python

from django import forms
from hunchworks import models
from hunchworks import json_views
from hunchworks.fields import TokenField


class UserForm(forms.ModelForm):
  #location_interests = TokenField(models.Location, json_views.locations, required=False)
  skills = TokenField(models.Skill, json_views.skills, required=False)
  languages = TokenField(models.Language, json_views.languages, required=False)

  class Meta:
    model= models.UserProfile
    exclude = ("user", "roles", "qualifications", "courses", "location_interests")
