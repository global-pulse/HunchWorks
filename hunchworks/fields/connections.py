#!/usr/bin/env python

from django import forms
from django.template.loader import render_to_string
from hunchworks import models


class MultipleConnectionWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    flat_widget = super(MultipleConnectionWidget, self)\
      .render(name, self._flat_value(value), attrs)

    return render_to_string(
      "includes/users/widget.html", {
        "flat_widget": flat_widget,
        "user_profile_list": self._value_objects(value)
      }
    )

  def value_from_datadict(self, data, files, name):
    keys = map(unicode.strip, data.get(name, "").split(","))
    return [int(key) for key in keys if key.isdigit()]

  def _value(self, value):
    return value or []

  def _flat_value(self, value):
    return ", ".join(map(unicode, self._value(value)))

  def _value_objects(self, value):
    return self.choices.queryset.order_by("name")

    #return self.choices.queryset.filter(
    #  pk__in=self._value(value)
    #)


class ConnectionsField(forms.ModelMultipleChoiceField):
  widget = MultipleConnectionWidget

  @classmethod
  def query_set(cls):
    return models.UserProfile.objects.all()

  def __init__(self, *args, **kwargs):
    super(ConnectionsField, self)\
      .__init__(self.query_set(), *args, **kwargs)
