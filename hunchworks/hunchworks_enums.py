#!/usr/bin/env python

"""Enums used throughout Hunchworks."""

__author__ = ('Leah',)
__license__ = 'GPLv3'

import inspect

class Error(Exception):
  pass


class EnumException(Error):
  pass


class Enum(object):
  """Class representing an enum in Python."""
  ##This has been commented out because leaving it as a global variable
  ## means that it is never reassigned when another class calls GetValues
  ## so your options are always the same. Map is now individually assigned
  ## in each class (redundant, but nessecary atm)
  #MAP = {}
  VALUE_LOOKUP = {}

  @classmethod
  def GetChoices(cls):
    """Returns a tuple representing the enum.

    Returns:
      A nested tuple, where each child tuple contains:
        (enum_value, user_facing_enum_value,)
    """
    enum_values = cls.GetEnumValues().items()
    return [(x[1], cls.GetValue(x[0]),) for x in enum_values]

  @classmethod
  def GetValue(cls, lookup):
    """Returns the user facing representation of an enum value.

    Args:
      lookup: The enum value to lookup.

    Returns:
      The user facing representation of the enum value.

    Raises:
      EnumException: Raised if the supplied value doesn't exist on the enum.
    """
    try:
      assert(lookup in cls.GetEnumValues().keys())
    except AssertionError:
      raise EnumException(
          'The supplied lookup value does not exist on the Enum')

    try:
      return cls.VALUE_LOOKUP[lookup]
    except KeyError:
      return lookup.title()

  @classmethod
  def GetEnumValues(cls):
    """Get's the Enum values as a dictionary.

    Returns:
      A dictionary wrapping the Enum values.
    """
    if not cls.MAP:
      # This is a bit of a hack - if the enum is defined in a module called
      # directly from the command line, it also has a __module__ attribute,
      # which the dummy object won't have.
      standard_attrs = ['__module__'] + dir(type('dummy', (object,), {}))
      class_attrs = inspect.getmembers(cls)
      for item in class_attrs:
         if (item[0] not in standard_attrs and
            not inspect.isroutine(item[1]) and
            not isinstance(item[1], (list, dict,))):
              cls.MAP[item[0]] = item[1]

    return cls.MAP


class ConnectionStatus(Enum):
  """Enum representing the possible statuses a user connection can take."""
  MAP = {}

  BLOCKED = 0
  FRIEND = 1
  ACCEPTED = 2


class UserTitle(Enum):
  """Enum representing the possible titles users can use."""
  MAP = {}

  MR = 0
  MRS = 1
  MS = 2

  FIELD_LOOKUP = {
    MR: 'Mr.',
    MRS: 'Mrs.',
    MS: 'Ms.',
    }


class PrivacyLevel(Enum):
  """Enum representing the various privacy levels available to users."""
  MAP = {}

  HIDDEN = 0
  CLOSED = 1
  OPEN = 2

  FIELD_LOOKUP = {
  	HIDDEN: 'Hidden',
  	CLOSED: 'Closed',
  	OPEN: 'Open',
  	}


class GroupType(Enum):
  """Enum representing the types of groups that can be made"""
  MAP = {}

  AD_HOC = 0
  ALUMNI = 1
  COMPLEMENT = 2
  CORPORATE = 3
  INTEREST = 4
  NON_PROFIT = 5

  FIELD_LOOKUP = {
    AD_HOC: 'Ad-Hoc',
    ALUMNI: 'Alumni',
    COMPLEMENT: 'Complement',
    CORPORATE: 'Corporate',
    INTEREST: 'Interest',
    NON_PROFIT: 'Non-Profit',
    }

class GroupPrivilege(Enum):
  ADMIN = 0
  MEMBER = 1

class LanguageOptions(Enum):

  MAP = {}

  ENGLISH = 0
  SPANISH = 1
  GERMAN = 2
  FRENCH = 3
  MANDARIN = 4

  FIELD_LOOKUP = {
    ENGLISH: 'English',
    SPANISH: 'Spanish',
    FRENCH: 'French',
    GERMAN: 'German',
    MANDARIN: 'Mandarin',
    }

class MessangerServices(Enum):

  MAP = {}

  AIM = 0
  YAHOO = 1
  MSN = 2
  IRC = 3
  MEEBO = 4

  FIELD_LOOKUP = {
    AIM: 'AIM',
    YAHOO: 'YAHOO',
    MSN: 'MSN',
    IRC: 'IRC',
    MEEBO: 'MEEBO',
    }


ATTACHMENT_TYPES = (
  ('Photo', 'Photo'),
  ('Link', 'Link'),
  ('Video', 'Video'),
)
