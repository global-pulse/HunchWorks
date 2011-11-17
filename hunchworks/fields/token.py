#!/usr/bin/env python

import json
from django import forms
from django.core.urlresolvers import reverse


class TokenWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    flat_value = ",".join(map(unicode, value or []))

    if hasattr(self, "search_view"):
      attrs["data-search-url"] = reverse(self.search_view)

    attrs["class"] = self._class_name(
      attrs.get("class"), "token-input")

    if value is not None:
      attrs["data-prepopulate"] = json.dumps([
        {"id": pk, "name": unicode(self.choices.queryset.get(pk=pk))}
        for pk in value
      ])

    return super(TokenWidget, self).render(
      name, flat_value, attrs)

  @staticmethod
  def _class_name(class_name=None, extra=None):
    return " ".join(filter(None, [class_name, extra]))

  def value_from_datadict(self, data, files, name):
    values = data.get(name, "").split(",")
    return self.clean_keys(values)

  def clean_keys(self, values):
    return [int(x) for x in values if x.strip().isdigit()]


class TokenField(forms.ModelMultipleChoiceField):
  widget = TokenWidget

  @staticmethod
  def _class_name(value):
    return value.replace(" ", "-")

  def __init__(self, model, search_view, *args, **kwargs):
    super(TokenField, self).__init__(model.objects.all(), *args, **kwargs)
    self.widget.class_name = self._class_name(model._meta.verbose_name_plural)
    self.widget.search_view = search_view