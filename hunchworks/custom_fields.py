#!/usr/bin/python2.7

"""Custom model fields for use with Djano."""

__author__ = ('Leah',)
__license__ = 'GPLv3'


from django.core import validators
from django.db.models import fields

UINT_64 = 0xffffffffffffffff
UINT_32 = 0xffffffff
UINT_8 = 0xff


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
