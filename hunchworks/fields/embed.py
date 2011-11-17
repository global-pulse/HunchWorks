#!/usr/bin/env python

from django import forms
from django.utils.safestring import mark_safe


class EmbedWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    widget = super(EmbedWidget, self).render(
      name, value, attrs)

    return mark_safe(u"""
      <div class="embed-widget">
        %s
      </div>
    """ % (widget))


class EmbedField(forms.CharField):
  widget = EmbedWidget
