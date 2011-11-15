#!/usr/bin/env python

from django import forms
from hunchworks import models
from hunchworks.fields import EvidencesField


class AlbumForm(forms.ModelForm):
  evidences = EvidencesField(required=False)

  class Meta:
    model = models.Album
