#!/usr/bin/env python

from django import forms
from hunchworks import models


class HunchCommentForm(forms.ModelForm):
  class Meta:
    model = models.Comment
    fields = ("text",)
