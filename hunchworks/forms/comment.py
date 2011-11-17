#!/usr/bin/env python

from django import forms
from hunchworks import models


class CommentForm(forms.ModelForm):
  class Meta:
    model = models.Comment
    fields = ("text", "hunch_evidence")
    widgets = {
      "hunch_evidence": forms.HiddenInput()
    }

  def save(self, creator=None):
    comment = super(CommentForm, self)\
      .save(commit=False)

    if creator is not None:
      comment.creator = creator

    comment.save()
    return comment
