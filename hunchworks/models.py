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

#import hunchworks_enums

from django.db import models

class Album(models.Model):
  """Class representing a collection of pictures in an album"""
  album_id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=45)
  class Meta:
    db_table = u'hw_album'

class Attachment(models.Model):
  """Class representing an attachment for a hunch"""
  attachment_id = models.IntegerField(primary_key=True)
  attachment_type = models.IntegerField()
  file_location = models.CharField(max_length=45)
  class Meta:
    db_table = u'hw_attachment'

class AlbumAttachments(models.Model):
  """Many to Many model joining Album and attachments"""
  album_attachments_id = models.IntegerField(primary_key=True)
  album_id = models.ForeignKey(Album)
  attachment = models.ForeignKey(Attachment)
  class Meta:
    db_table = u'hw_album_attachments'

class Class(models.Model):
  """Class representing a educational class taken that may or may not have
  been at a college"""
  class_id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=45)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  class Meta:
    db_table = u'hw_class'

class Education(models.Model):
  """Class representing a degree or qualification obtained by a user."""
  education_id = models.IntegerField(primary_key=True)
  school = models.CharField(max_length=255)
  qualification = models.CharField(max_length=100)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  class Meta:
    db_table = u'hw_education'
  
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
  language_id = models.IntegerField(primary_key=True)
  name = models.CharField(unique=True, max_length=45)
  class Meta:
    db_table = u'hw_language'
  
class Location(models.Model):
  """Class representing a location used by the application.

  These locations are derived from either:
  1. Open Street Map Nominatim API (
     http://wiki.openstreetmap.org/wiki/Nominatim)
  2. Google Maps Geocoding API (
     http://code.google.com/apis/maps/documentation/geocoding/#JSON)

  That decision is still TBD, so for now this class is a stub.
  """
  location_id = models.IntegerField(primary_key=True)
  name = models.CharField(unique=True, max_length=45)
  class Meta:
    db_table = u'hw_location'
  
class UserInstantMessenger(models.Model):
  """Class representing the users Instant Messenger and the service under which
  the messenger is provided"""
  user_messenger_id = models.IntegerField(primary_key=True)
  screen_name = models.CharField(max_length=45)
  messenger_service = models.IntegerField()
  class Meta:
    db_table = u'hw_user_messenger'

class User(models.Model):
  """Class representing a Hunchworks user."""
  user_id = models.IntegerField(primary_key=True)
  email = models.CharField(unique=True, max_length=45)
  first_name = models.CharField(max_length=25)
  last_name = models.CharField(max_length=50)
  title = models.IntegerField()
  bio_text = models.TextField(blank=True)
  work_phone = models.CharField(max_length=30, blank=True)
  skype_name = models.CharField(max_length=30, blank=True)
  instant_messenger_id = models.ForeignKey(UserInstantMessenger, null=True, blank=True)
  website = models.CharField(max_length=100, blank=True)
  profile_picture = models.CharField(max_length=100, blank=True)
  show_profile_reminder = models.IntegerField()
  privacy = models.IntegerField()
  default_language_id = models.ForeignKey(Language)
  skills = models.ManyToManyField('Skill', through='UserSkills')
  education = models.ManyToManyField('Education', through='UserEducation')
  classes = models.ManyToManyField('Class', through='UserClasses')
  location_interests = models.ManyToManyField(
  'Location', through='LocationInterests')
  roles = models.ManyToManyField('Role', through='UserRoles')
  hunches = models.ManyToManyField('Hunch', through='HunchConnections')
  invited_users = models.ManyToManyField('InvitedUser', through='UserInvites')
  groups = models.ManyToManyField('Group', through='GroupConnections')
  #@property
  #def title_text(self):
  #  return hunchworks_enums.UserTitle.GetValue(self.title)
  class Meta:
    db_table = u'hw_user'

class Hunch(models.Model):
  """Class representing a Hunch."""
  hunch_id = models.IntegerField(primary_key=True)
  time_created = models.DateTimeField()
  status = models.IntegerField()
  title = models.CharField(max_length=100)
  privacy = models.IntegerField()
  language = models.ForeignKey(Language, null=True, blank=True)
  location = models.ForeignKey(Location, null=True, blank=True)
  description = models.TextField(blank=True)
  creator_id = models.ForeignKey(User, related_name='%(class)s_creator_id')
  skills = models.ManyToManyField('Skill', through='HunchSkills')
  groups = models.ManyToManyField('Group', through='HunchGroups')
  users = models.ManyToManyField('User', through='HunchConnections')
  evidence = models.ManyToManyField('Evidence')
  invited_users = models.ManyToManyField('InvitedUser', through='HunchInvites')
  class Meta:
    db_table = u'hw_hunch'

class Evidence(models.Model):
  """Class representing a response to the hunch"""
  evidence_id = models.IntegerField(primary_key=True)
  hunch_id = models.ForeignKey(Hunch, related_name='%(class)s_hunch_id')
  creator_id = models.ForeignKey(User)
  time_created = models.DateTimeField()
  description = models.TextField(blank=True)
  albums = models.ManyToManyField('Album', through='EvidenceAlbums')
  attachments = models.ManyToManyField('Attachment', through='EvidenceAttachments')
  class Meta:
    db_table = u'hw_evidence'

class EvidenceAlbums(models.Model):
  """Many to Many model joining Evidence and Album together"""
  evidence_albums_id = models.IntegerField(primary_key=True)
  album_id = models.ForeignKey(Album)
  evidence_id = models.ForeignKey(Evidence)
  class Meta:
    db_table = u'hw_evidence_albums'

class EvidenceAttachments(models.Model):
  """Many to Many model joining evidence and attachments."""
  evidence_attachment_id = models.IntegerField(primary_key=True)
  attachment_id = models.ForeignKey(Attachment)
  evidence_id = models.ForeignKey(Evidence)
  class Meta:
    db_table = u'hw_evidence_attachments'

class Group(models.Model):
  """Class representing a logical grouping of Hunchworks users."""
  group_id = models.IntegerField(primary_key=True)
  name = models.CharField(unique=True, max_length=100, blank=True)
  group_type = models.IntegerField()
  privacy = models.IntegerField()
  location = models.ForeignKey(Location, null=True, blank=True)
  logo = models.CharField(max_length=100, blank=True)
  hunches = models.ManyToManyField('Hunch', through='HunchGroups')
  users = models.ManyToManyField('User', through='GroupConnections')
  class Meta:
    db_table = u'hw_group'

class GroupConnections(models.Model):
  """Many to Many model joining groups with their member users."""
  group_user_id = models.IntegerField(primary_key=True)
  user_id = models.ForeignKey(User)
  group_id = models.ForeignKey(Group)
  access_level = models.IntegerField()
  trust_from_user = models.IntegerField()
  trust_from_group = models.IntegerField()
  receive_updates = models.IntegerField()
  status = models.IntegerField()
  class Meta:
    db_table = u'hw_group_connections'

class HunchConnections(models.Model):
  """Many to Many model joining Hunch and User together"""
  hunch_connections_id = models.IntegerField(primary_key=True)
  hunch_id = models.ForeignKey(Hunch)
  user_id = models.ForeignKey(User)
  status = models.IntegerField()
  class Meta:
    db_table = u'hw_hunch_connections'

class HunchGroups(models.Model):
  """Many to Many model joining Hunch and Group together"""
  hunch_groups_id = models.IntegerField(primary_key=True)
  group_id = models.ForeignKey(Group)
  hunch_id = models.ForeignKey(Hunch)
  status = models.IntegerField()
  class Meta:
    db_table = u'hw_hunch_groups'
  
class InvitedUser(models.Model):
  """Class representing a master list of all users ever invited to the system
  and their respective user id's if they created an account."""
  invited_users_id = models.IntegerField(primary_key=True)
  user_id = models.ForeignKey(User, null=True, blank=True)
  email = models.CharField(unique=True, max_length=45)
  class Meta:
    db_table = u'hw_invited_user'

class HunchInvites(models.Model):
  """Many to Many model joining Hunch and Invited Users together"""
  hunch_invites_id = models.IntegerField(primary_key=True)
  invited_user_id = models.ForeignKey(InvitedUser)
  hunch_id = models.ForeignKey(Hunch)
  status = models.IntegerField()
  class Meta:
    db_table = u'hw_hunch_invites'
  
class Skill(models.Model):
  """Class representing a skill possessed by a user, e.g. HTML."""
  skill_id = models.IntegerField(primary_key=True)
  skill = models.CharField(unique=True, max_length=100)
  is_language = models.IntegerField()
  is_technical = models.IntegerField()
  class Meta:
    db_table = u'skill'

class HunchSkills(models.Model):
  """Many to Many model joining hunches and skills.

  This model represents the skill-set required to progress a hunch and the skill
  level needed for each skill.
  """
  hunch_skill_id = models.IntegerField(primary_key=True)
  hunch_id = models.ForeignKey(Hunch)
  skill_id = models.ForeignKey(Skill)
  level = models.IntegerField()
  class Meta:
    db_table = u'hw_hunch_skills'

class LocationInterests(models.Model):
  """Many to Many model joining User and Location together for their list
  of locations they are interested in"""
  location_interests_id = models.IntegerField(primary_key=True)
  user_id = models.ForeignKey(User)
  location_id = models.ForeignKey(Location)
  class Meta:
    db_table = u'hw_location_interests'

class Organization(models.Model):
  """Class representing an external organization (UNDP etc.)."""
  organization_id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=125)
  abbreviation = models.CharField(max_length=15)
  group_id = models.ForeignKey(Group)
  location_id = models.ForeignKey(Location, null=True, blank=True)
  class Meta:
    db_table = u'hw_organization'

class Role(models.Model):
  """Class representing a role held by a given user."""
  role_id = models.IntegerField(primary_key=True)
  organization = models.ForeignKey(Organization)
  title = models.CharField(max_length=255)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  description = models.TextField(blank=True)
  class Meta:
    db_table = u'hw_role'

class UserClasses(models.Model):
  """Many to Many model joining User and Class together"""
  user_class_id = models.IntegerField(primary_key=True)
  user_id = models.ForeignKey(User)
  class_id = models.ForeignKey(Class)
  class Meta:
    db_table = u'hw_user_classes'

class UserConnections(models.Model):
  """Class representing a personal connection between two users."""
  user_connection_id = models.IntegerField(primary_key=True)
  user_a_id = models.ForeignKey(User, related_name='%(class)s_user_a_id')
  user_b_id = models.ForeignKey(User, related_name='%(class)s_user_b_id')
  status = models.IntegerField()
  class Meta:
    db_table = u'hw_user_connections'

class UserEducation(models.Model):
  """Many to Many model representing a user's degrees / education."""
  user_education_id = models.IntegerField(primary_key=True)
  user_id = models.ForeignKey(User)
  education_id = models.ForeignKey(Education)
  class Meta:
    db_table = u'hw_user_education'

class UserInvites(models.Model):
  """Many to Many model joining User and Invited User together for the users 
  invited people list"""
  user_invites_id = models.IntegerField(primary_key=True)
  user_id = models.ForeignKey(User)
  invited_users = models.ForeignKey(InvitedUser)
  status = models.IntegerField()
  class Meta:
    db_table = u'hw_user_invites'

class UserRoles(models.Model):
  """Many To many model representing a user's roles or positions."""
  user_role_id = models.IntegerField(primary_key=True)
  user_id = models.ForeignKey(User)
  role_id = models.ForeignKey(Role)
  class Meta:
    db_table = u'hw_user_roles'

class UserSkills(models.Model):
  """Many to Many model joining user and skill.

  This model represents the skill-set of users, and also indicates their level
  of expertise in a given skill. Currently, expertise is two-tier; users are
  either skilled or expert in a given area.
  """
  user_skill_id = models.IntegerField(primary_key=True)
  user_id = models.ForeignKey(User)
  skill_id = models.ForeignKey(Skill)
  level = models.IntegerField()
  class Meta:
    db_table = u'hw_user_skills'
  
# Getters for setting the default values for ForeignKeys on other models.
def GetDefaultLanguage():
  return Language.objects.get(pk='en')


def GetHunchGroup():
  # TODO(leah): Set this up to auto-create a new group, taking names, owners
  #       etc. from the hunch. Need to figure out how to pass that stuff
  #       in.
  pass
