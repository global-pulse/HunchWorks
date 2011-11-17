#!/usr/bin/env python

from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from hunchworks import models


class VoteChoiceRenderer(widgets.RadioFieldRenderer):
  """
  Identical to Django's RadioFieldRenderer, with the addition of a "selected"
  class to the <li> containing the selected radio button, for easier styling.
  """

  def _ul(self):
    return '<ul>%s</ul>' % "".join(
      map(self._li, self))

  def _css_class(self, widget):
    label = widget.choice_label.lower().replace(" ", "-")
    css_class = re.sub("[^a-z\-]+", "", label)

    if(self.value == widget.choice_value):
      css_class += " selected"

    return css_class

  def _li(self, widget):
    return '<li class="%s">%s</li>' % (
      self._css_class(widget), unicode(widget))

  def render(self):
    return mark_safe('<div class="vote-widget">%s</div>' % (
      self._ul()))


class VoteWidget(forms.RadioSelect):
  renderer = VoteChoiceRenderer


class VoteField(forms.ChoiceField):
  choices = models.SUPPORT_CHOICES
  widget = VoteWidget
