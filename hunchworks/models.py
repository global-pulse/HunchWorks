#!/usr/bin/python2.7

# Date: 2011-06-15
# License:  This  program  is  free  software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the  Free Software Foundation; either version 3 of the License, or (at your
# option)  any later version. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.

"""Enums used throughout Hunchworks."""

__author__ = ('Chris',)
__license__ = 'GPLv3'

import hunchworks_enums

from django.db import models

# TODO(Texas:2011-06-15) Skills list likely to be needed in future
# TODO(Texas:2011-06-15) Expertise list likely to be needed in future
# TODO(Texas:2011-06-15) Instant messenger Types supported list likely needed
# TODO(Texas:2011-06-15) Evidence.strength Choices might be needed in future


class User(models.Model):
  """Class representing a Hunchworks user."""
  user_id = models.IntegerField(primary_key=True, db_column='user_id')
  # DISCUSS: Are we going to manage our own login system or rely on other
  #          services?
  # TODO(leah): If we're rolling our own, research entropic salting for
  #             passwords.
  # password = models.CharField(max_length=100)

  # Basic details about the user.
  email = models.EmailField(max_length=100)
  first_name = models.CharField(max_length=25)
  last_name = models.CharField(max_length=50)
  title = models.IntegerField(
      choices=hunchwork_enums.UserTitle.GetChoices(), blank=True, null=True)
  # DISCUSS: Do we want to track location history? If so, I'd up this to M2M
  #          field, with a through table that tracks status.
  location = models.ForeignKey('Location', db_column='location_id')
  # DISCUSS: Do we care that much about their hometown?
  hometown_id = models.ForeignKey(
      'Location', blank=True, null=True, db_column='hometown_id')

  # Skills and talents.
  skills = models.ManyToManyField('Skill', through='UserSkills')
  # DISCUSS: This seems like it should be treated as any other skill, with an
  #          is_language attribute on the Skill class to manage it.
  # languages_known = models.ManyToManyField('Language')

  # Detailed user information.
  education = models.ManyToManyField('Education')
  location_interests = models.ManyToManyField('Location')
  # DISCUSS: This seems like it should be split into multiple, smaller segments.
  #          These should be structured to extract more usable / directed info
  #          from the user.
  #
  # DISCUSS: Secondly, is there a reason why varchar(1000) fields are favored?
  #          Storing large chunks of data inline in this way is generally bad
  #          practice without a compelling reason. Generally, a TEXT field would
  #          be used for this kind of storage, although that isn't stored inline
  #          with the table, so does incur an additional cost. However, for many
  #          common cases (e.g. navigating the social graph), that's a good
  #          thing.
  bio_text = models.CharField(max_length=1000, blank=True)
  roles = models.ManyToManyField('Role', through='UserRole')

  # Contact details.
  # DISCUSS: We're going to have to think pretty hard about how to make this
  #          work well. It's somewhat painful validating phone numbers from a
  #          large # of countries.
  work_phone = models.CharField(max_length=30, blank=True, null=True)
  skype_name = models.CharField(max_length=30, blank=True, null=True)
  # DISCUSS: What is this going to be used for? I assume handles on various IM
  #          services? But that doesn't join up with the comment re. an IM
  #          option list...
  # TODO(Texas:2011-06-15) Add instant messenger option list when created
  instant_messenger = models.CharField(max_length=30, blank=True, null=True)
  # DISCUSS: Do we want to validate that these sites actually exist? If so, we
  #          can turn verify_exists=True on.
  website = models.URLField(max_length=200, blank=True, null=True)

  # App settings for the user.
  # DISCUSS: This is for sometime in the future, but we should think about
  #          scalable static content serving.
  profile_picture = models.URLField(max_length=200, blank=True, null=True)
  show_profile_reminder = models.BooleanField(default=True)
  privacy = models.IntegerField(
      default=hunchworks_enums.PrivacyLevel.HIDDEN,
      choices=hunchworks_enums.PrivacyLevel.GetChoices())
  default_language_id = models.ForeignKey(
      'Language', default=GetDefaultLanguage, db_column='default_language_id')
  # DISCUSS: This is just a special case of a user connection.
  # blocked_users = models.CharField(max_length=1000, blank=True)

  # DISCUSS: These are also all just special cases of user connections. It would
  #          be cleaner to handle these with statuses / connection types.
  # invited_by = models.ForeignKey('self', blank=True, null=True)
  # has_invited = models.ManyToManyField('self', through='UserInvite')

  @property
  def title_text(self):
    return hunchworks_enums.UserTitle.GetValue(self.title)


class UserConnection(models.Model):
  """Class representing a personal connection between two users."""
  user_a_id = models.ForeignKey(
      User, db_column='user_a_id', related_name='%(class)s_user_a_id')
  user_b_id = models.ForeignKey(
      User, db_column='user_b_id', related_name='%(class)s_user_b_id')

  status = models.IntegerField(
      choices=hunchworks_enums.ConnectionStatus.GetChoices())

  # TODO(leah): Add in invited_by etc. support following discussion re. this
  #             table.

  # DISCUSS: What does it mean to follow someone in this context?
  # user_one_following_user_two = models.IntegerField()
  # user_two_following_user_one = models.IntegerField()

  # DISCUSS: My read on these fields is that they're being used to represent
  #          the quality / level of connection between a given user, e.g. at
  #          FRIEND / COLLEAGUE level and above contact info should be visible.
  #          Per my comments on the user model, I'd suggest moving to a
  #          explicit status approach, so that BLOCKED etc. is possible
  # user_one_shared_contact_info = models.IntegerField()
  # user_two_shared_contact_info = models.IntegerField()


class UserEducation(models.Model):
  """Many to Many model representing a user's degrees / education."""
  user = models.ForeignKey('User', db_column='user_id')
  education = models.ForeignKey('Education', db_column='education_id')


# DISCUSS: Do we care about < university level education?
class Education(models.Model):
  """Class representing a degree or qualification obtained by a user."""
  school = models.CharField(max_length=255)
  qualification = models.CharField(max_length=100)
  # DISCUSS: How do we want to handle this? Start out with some fixed set of
  #          subjects and go from there, or make it free text?
  # fields = models.CharField(max_length=10)
  start_date = models.DateField(blank=True, null=True)
  end_date = models.DateField(blank=True, null=True)


class UserRole(models.Model):
  """Many To many model representing a user's roles or positions."""
  user = models.ForeignKey('User', db_column='user_id')
  role = models.ForeignKey('Role', db_column='role_id')


class Role(models.Model):
  """Class representing a role held by a given user."""
  organization = models.ForeignKey('Organization', db_column='organization_id')
  title = models.CharField(max_length=255)
  location = models.ForeignKey('Location', db_column='location_id')
  started = models.DateField()
  ended = models.DateField(blank=True, null=True)
  description = models.TextField()


# DISCUSS: How should we verify the org ownership?
class Organization(models.Model):
  """Class representing an external organization (UNDP etc.)."""
  name = models.CharField(max_length=125)
  abbreviation = models.CharField(max_length=12)
  # All organizations are associated with a group by default.
  group_id = models.ForeignKey(
      'Group', db_column='group_id', default=GetHunchGroup)
  # TODO(leah): Add location, contact fields etc.


class UserSkills(models.Model):
  """Many to Many model joining user and skill.

  This model represents the skill-set of users, and also indicates their level
  of expertise in a given skill. Currently, expertise is two-tier; users are
  either skilled or expert in a given area.
  """
  user_skill_id = models.IntegerField(
      primary_key=True, db_column='user_skill_id')
  user_id = models.ForeignKey('User', db_column='user_id')
  skill_id = models.ForeignKey('Skill', db_column='skill_id')
  level = models.IntegerField(choices=hunchworks_enums.SkillLevel.GetChoices())


class Skill(models.Model):
  """Class representing a skill possessed by a user, e.g. HTML."""
  skill_id = models.IntegerField(primary_key=True, db_column='skill_id')
  skill = models.CharField(max_length=100)
  is_language = models.BooleanField()
  is_technical = models.BooleanField()


# TODO(leah): Figure out what full list of languages to support for the purposes
#             of user declared known languages. Also, figure out where to get
#             a complete language code --> language name mapping.
class Language(models.Model):
  """Class representing a language supported by the application.

  This table is provided during development to ease integration of i18n and
  translation features. It provides a mapping from a purported language code to
  the actual language code to use. This allows us to use English by default
  everywhere, whilst plumbing in the i18n architecture from the beginning.

  Languages are coded per the Django global_settings module
  (http://goo.gl/sp5OI), rather than the full i18n values (http://goo.gl/DgmM).
  Django uses one level language tags generally, in this application these map
  to:
  1. en: en-US (use US English)
  2. es: es-ES (use Iberian Spanish)
  3. fr: fr-FR
  4. de: de-DE
  5. zh-cn: zh-cn (use simplified Chinese)
  """
  code = models.CharField(max_length=5, primary_key=True, db_column='code')
  dev_code = models.CharField(max_length=5)


class Location(models.Model):
  """Class representing a location used by the application.

  These locations are derived from either:
    1. Open Street Map Nominatim API (
       http://wiki.openstreetmap.org/wiki/Nominatim)
    2. Google Maps Geocoding API (
       http://code.google.com/apis/maps/documentation/geocoding/#JSON)

  That decision is still TBD, so for now this class is a stub.
  """
  location_id = models.IntegerField(primary_key=True, db_column='location_id')
  name = models.CharField(max_length=100)


class Hunch(models.Model):
  """Class representing a Hunch."""
  hunch_id = models.IntegerField(primary_key=True, db_column='hunch_id')
  # All hunches are also Groups, so auto-create a group when a hunch is created.
  group_id = models.ForeignKey(
      'Group', db_column='group_id', default=GetHunchGroup)
  time_created = models.DateTimeField()
  status = models.IntegerField(
      choices=hunchworks_enums.HunchStatus.GetChoices(),
      default=hunchworks_enums.HunchStatus.UNDETERMINED)
  # DISCUSS: We should figure out some logic for ownership on groups / hunches.
  #          For example, it seems like they should allow for > 1 owner, admin
  #          etc. I'm inclined to delegate all that stuff to the Group model and
  #          have the Hunch just figure stuff out from there.
  creator_id = models.ForeignKey(User)
  title = models.CharField(max_length=100)
  privacy = models.IntegerField(
      choices=hunchworks_enums.PrivacyLevel.GetChoices(),
      default=hunchworks_enums.PrivacyLevel.HIDDEN)

  language = models.ForeignKey('Language', default='en')
  location = models.ForeignKey('Location', blank=True, null=True)

  tags = models.CharField(max_length=100, blank=True)
  # DISCUSS: Per the User bio, let's try and split this up into more structured
  #          elements + also consider a TEXT field.
  description = models.CharField(max_length=1000, blank=True)

  needed_skills = models.ManyToManyField('Skill', through='HunchSkills')


class HunchSkills(models.Model):
  """Many to Many model joining hunches and skills.

  This model represents the skill-set required to progress a hunch and the skill
  level needed for each skill.
  """
  hunch_skill_id = models.IntegerField(
      primary_key=True, db_column='hunch_skill_id')
  hunch_id = models.ForeignKey('Hunch', db_column='hunch_id')
  skill_id = models.ForeignKey('Skill', db_column='skill_id')
  level = models.IntegerField(choices=hunchworks_enums.SkillLevel.GetChoices())


class Group(models.Model):
  """Class representing a logical grouping of Hunchworks users."""
  group_id = models.IntegerField(primary_key=True, db_column='group_id')
  name = models.CharField(max_length=100)
  group_type = models.IntegerField(
      choices=hunchworks_enums.Group.GetChoices())
  privacy = models.IntegerField(
      default=hunchworks_enums.PrivacyLevel.HIDDEN,
      choices=hunchworks_enums.PrivacyLevel.GetChoices())
  location = models.ForeignKey('Location', blank=True, null=True)
  logo = models.CharField(max_length=100, blank=True)
  members = models.ManyToManyField('User', through='GroupUsers')


class GroupUsers(models.Model):
  """Many to Many model joining groups with their member users."""
  user_id = models.ForeignKey('User', db_column='user_id')
  group_id = models.ForeignKey('Group', db_column='group_id')
  access_level = models.IntegerField(
      default=hunchworks_enums.GroupPrivilege.Member,
      choices=hunchworks_enums.GroupPrivilege.GetChoices())
  trust_from_user = models.IntegerField()
  trust_from_group = models.IntegerField()
  recieve_updates = models.IntegerField()
  # DISCUSS: Let's figure this out another way, e.g. maintaining this table as
  #          a history, with an associated status.
  # invited_by = models.CharField(max_length=1000, blank=True)
  # has_invited = models.CharField(max_length=1000, blank=True)


# DISCUSS: The next classes confuse me. I'm really not sure how the Hunch,
#          Attachment, Album, Attachment relationship is supposed to work...

# DISCUSS: What is this? It would be good to have docstrings to briefly explain
#          what each object is...
class Album(models.Model):
  album_id = models.IntegerField(primary_key=True)
  hunch_id = models.ForeignKey(Hunch)
  name = models.CharField(max_length=30)


class Evidence(models.Model):
  evidence_id = models.IntegerField(primary_key=True, db_column='evidence_id')
  hunch_id = models.ForeignKey('Hunch', db_column='hunch_id')
  uploader_id = models.ForeignKey('User', db_column='user_id')
  # DISCUSS: Per the other points re. big text fields.
  # description = models.CharField(max_length=1000, blank=True, null=True)
  text = models.CharField(max_length=1000, blank=True)
  time_created = models.DateTimeField()
  attachments = models.ManyToManyField(
      'Attachment', through='EvidenceAttachment')
  # TODO(Texas:2011-06-15) Add language list in the future
  language = models.CharField(max_length=30, blank=True)
  # TODO(Texas:2011-06-15) Add Strength choices if created
  strength = models.IntegerField()


class EvidenceAttachment(models.Model):
  """Many to Many model joining evidence and attachments."""
  evidence_attachment_id = models.IntegerField(
      primary_key=True, db_column='evidence_attachment_id')
  evidence_id = models.ForeignKey('Evidence', db_column='evidence_id')
  attachment_id = models.ForeignKey('Evidence', db_column='evidence_id')


# DISCUSS: This should probably be re-named. It's basically just here to
#          represent some kind of static resource on our system right? In which
#          case, it's likely that the set of all static resources we end up
#          serving > the set that's uploaded as part of a hunch, e.g. the logo
#          for a group.
class Attachment(models.Model):
  hunch_id = models.ForeignKey(Hunch)
  evidence_id = models.ForeignKey(Evidence)
  file_location = models.CharField(max_length=100)
  attachment_type = models.CharField(
      max_length=15, choices=hunchworks_enums.ATTACHMENT_TYPES)
  album_id = models.ForeignKey(Album, null=True, blank=True)
  attachment_id = models.IntegerField(primary_key=True)


# DISCUSS: I'm not convinced that we should do our own messaging system. It's
#          fairly easy to use the user's inbox as the messaging platform
#          without exposing their address directly. Basically, we just generate
#          a hash / user_id as a unique address on our domain, and then proxy /
#          route e-mails back and forth via that.
class Message(models.Model):
  from_user_id = models.ForeignKey(User)
  to_user_id = models.ForeignKey(User, related_name='%(class)s_toUserId')
  text = models.CharField(max_length=1000)
  message_id = models.IntegerField(primary_key=True)


# Getters for setting the default values for ForeignKeys on other models.
def GetDefaultLanguage():
  return Language.objects.get(pk='en')


def GetHunchGroup():
  # TODO(leah): Set this up to auto-create a new group, taking names, owners
  #             etc. from the hunch. Need to figure out how to pass that stuff
  #             in.
  pass
