#!/usr/bin/env python

from django import forms
from django.template.loader import render_to_string
from hunchworks import models


class EvidenceWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    flat_widget = super(EvidenceWidget, self)\
      .render(name, value, attrs)

    try:
      object_list = [self.choices.queryset.get(pk=value)]

    except:
      object_list = []

    return render_to_string(
      "evidences/widget.html", {
        "flat_widget": flat_widget,
        "help_text": self._help(),
        "object_list": object_list,
        "variety": "one"
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
