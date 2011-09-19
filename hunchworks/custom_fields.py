#!/usr/bin/env python

from django.core import validators
from django.db.models import fields
from django import forms


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