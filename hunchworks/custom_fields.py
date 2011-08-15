#!/usr/bin/python2.7

"""Custom model fields for use with Djano."""

__author__ = ('Leah',)
__license__ = 'GPLv3'


from django.core import validators
from django.db.models import fields
from django import forms

UINT_64 = 0xffffffffffffffff
UINT_32 = 0xffffffff
UINT_8 = 0xff

class MultiEmailField(forms.Field):
  def to_python(self, value):
    "Normalize data to a list of strings."

    # Return an empty list if no input was given.
    if not value:
      return []
    return value.split(',')

  def validate(self, value):
    "Check if value consists only of valid emails."

    # Use the parent's handling of required fields, etc.
    super(MultiEmailField, self).validate(value)

    for email in value:
      validators.validate_email(email)

class UnsignedBigIntegerField(fields.PositiveIntegerField):
  """mySQL unsigned BIGINT field."""

  def __init__(self, *args, **kwargs):
    super(UnsignedBigIntegerField, self).__init__(*args, **kwargs)
    self.validators.append(validators.MaxValueValidator(UINT_64))
    self.validators.append(validators.MinValueValidator(0))

  def get_internal_type(self):
    return 'UnsignedBigIntegerField'

  def db_type(self):
    return 'BIGINT UNSIGNED'


class UnsignedIntegerField(fields.PositiveIntegerField):
  """mySQL unsigned INTEGER field."""

  def __init__(self, *args, **kwargs):
    super(UnsignedBigIntegerField, self).__init__(*args, **kwargs)
    self.validators.append(validators.MaxValueValidator(UINT_64))
    self.validators.append(validators.MinValueValidator(0))

  def get_internal_type(self):
    return 'UnsignedIntegerField'

  def db_type(self):
    return 'INTEGER UNSIGNED'


class UnsignedTinyIntegerField(fields.PositiveIntegerField):
  """mySQL unsigned TINYINT field."""

  def __init__(self, *args, **kwargs):
    super(UnsignedBigIntegerField, self).__init__(*args, **kwargs)
    self.validators.append(validators.MaxValueValidator(UINT_8))
    self.validators.append(validators.MinValueValidator(0))

  def get_internal_type(self):
    return 'UnsignedTinyIntegerField'

  def db_type(self):
    return 'TINYINT UNSIGNED'
