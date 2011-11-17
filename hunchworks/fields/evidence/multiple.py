#!/usr/bin/env python

from django import forms
from django.template.loader import render_to_string
from hunchworks import models


class MultipleEvidenceWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    flat_widget = super(MultipleEvidenceWidget, self)\
      .render(name, self._flat_value(value), attrs)

    return render_to_string(
      "evidences/widget.html", {
        "flat_widget": flat_widget,
        "help_text": self._help(),
        "evidence_list": self._value_objects(value),
        "variety": "many"
      }
    )

  def value_from_datadict(self, data, files, name):
    keys = map(unicode.strip, data.get(name, "").split(","))
    return [int(key) for key in keys if key.isdigit()]

  def _help(self):
    return "If JavaScript is disabled, enter evidence IDs separated by commas."

  def _value(self, value):
    return value or []

  def _flat_value(self, value):
    return ", ".join(map(unicode, self._value(value)))

  def _value_objects(self, value):
    return self.choices.queryset.filter(
      pk__in=self._value(value)
    )


class EvidencesField(forms.ModelMultipleChoiceField):
  widget = MultipleEvidenceWidget

  @classmethod
  def query_set(cls):
    return models.Evidence.objects.all()

  def __init__(self, *args, **kwargs):
    super(EvidencesField, self)\
      .__init__(self.query_set(), *args, **kwargs)
