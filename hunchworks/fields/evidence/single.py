#!/usr/bin/env python

from django import forms
from django.template.loader import render_to_string
from hunchworks import models


class EvidenceWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    flat_widget = super(EvidenceWidget, self)\
      .render(name, value, attrs)

    try:
      evidence = self.choices.queryset.get(pk=value)
      previews = [self.render_one(evidence)]

    except:
      previews = []

    return render_to_string(
      "evidences/widget.html", {
        "flat_widget": flat_widget,
        "help_text": self._help(),
        "previews": previews,
        "variety": "one"
      }
    )

  def render_one(self, evidence):
    return render_to_string(
      "evidences/short.html", {
        "evidence": evidence
      }
    )

  def _help(self):
    return "If JavaScript is disabled, enter an evidence ID."


class EvidenceField(forms.ModelChoiceField):
  widget = EvidenceWidget

  @classmethod
  def query_set(cls):
    return models.Evidence.objects.all()

  def __init__(self, *args, **kwargs):
    super(EvidenceField, self)\
      .__init__(self.query_set(), *args, **kwargs)
