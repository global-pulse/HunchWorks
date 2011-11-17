#!/usr/bin/env python

from django import forms
from django.db import transaction
from hunchworks import models
from hunchworks import json_views
from hunchworks.fields import TokenField, EmbedField, LocationField


class EvidenceForm(forms.ModelForm):
  tags = TokenField(models.Tag, json_views.tags, required=False,
    help_text="Tags that you think would help others search for or find this Evidence")

  link = EmbedField(
    help_text='Enter an URL to be embedded. You can find a list of supported ' +
              'providers at <a href="http://embed.ly/providers">Embedly</a>.')

  location = LocationField(required=False,
    help_text="If the evidence is relative to a specific location, you can mark it here.")

  class Meta:
    model = models.Evidence
    fields = (
      "title", "description", "link", "tags", "location"
    )

  def save(self, creator=None):
    with transaction.commit_on_success():
      evidence = super(EvidenceForm, self)\
        .save(commit=False)

      if creator is not None:
        evidence.creator = creator

      evidence.save()
      return evidence