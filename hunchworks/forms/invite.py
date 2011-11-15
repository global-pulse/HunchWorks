#!/usr/bin/env python

from django import forms
from django.core import validators
from hunchworks import models


class MultiEmailField(forms.Field):
  def to_python(self, value):
    "Normalize data to a list of strings."

    # Return an empty list if no input was given.
    if not value:
      return []
    return map(unicode.strip, value.split(','))

  def validate(self, value):
    "Check if value consists only of valid emails."

    # Use the parent's handling of required fields, etc.
    super(MultiEmailField, self).validate(value)

    for email in value:
      validators.validate_email(email)


class InviteForm(forms.Form):
  invited_emails = MultiEmailField(widget=forms.Textarea(
    attrs={'cols': 30, 'rows': 10}))

  def save(self, user_id, hunch=None, *args, **kwargs):
    user = models.UserProfile.objects.get(pk=user_id)
    #hunch = models.Hunch.objects.get(pk=hunch_id)

    #TODO( Chris: 8-15-2011): figure out how ot introspect invited_emails object instead
    # of using email_input
    for email_input in self.cleaned_data['invited_emails']:
      invitation = models.Invitation(
      invited_by = user,
      email = email_input,
      #hunch = hunch,
      )
      invitation.save()
