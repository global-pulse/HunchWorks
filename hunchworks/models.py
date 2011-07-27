#!/usr/bin/python2.7

# Date: 2011-06-15
# License:  This  program  is  free  software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the  Free Software Foundation; either version 3 of the License, or (at your
# option)  any later version. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.

__author__ = ('Chris',)
__license__ = 'GPLv3'

"""Enums used throughout Hunchworks."""
import hunchworks_enums

from django.db import models

class HwAlbum(models.Model):
  """Class representing a collection of pictures in an album"""
  album_id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=45)
  evidence = models.ManyToManyField('HwEvidence', through='HwEvidenceAlbums')
  class Meta:
    db_table = u'hw_album'
    
class HwAttachment(models.Model):
  """Class representing an attachment for a hunch"""
  attachment_id = models.IntegerField(primary_key=True)
  attachment_type = models.IntegerField()
  file_location = models.CharField(max_length=100)
  albums = models.ManyToManyField('HwAlbum', through='HwAlbumAttachments')
  evidence = models.ManyToManyField(
    'HwEvidence', through='HwEvidenceAttachments')
  class Meta:
    db_table = u'hw_attachment'
    
class HwAlbumAttachments(models.Model):
  """Many to Many model joining Album and attachments"""
  album = models.ForeignKey(HwAlbum)
  attachment = models.ForeignKey(HwAttachment)
  class Meta:
    db_table = u'hw_album_attachments'

class HwClass(models.Model):
  """Class representing a educational class taken that may or may not have
  been at a college"""
  class_id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=45)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  users = models.ManyToManyField('HwUser', through='HwEducationConnections')
  class Meta:
    db_table = u'hw_class'
    
class HwEducation(models.Model):
  """Class representing a degree or qualification obtained by a user."""
  education_id = models.IntegerField(primary_key=True)
  school = models.CharField(max_length=255)
  qualification = models.CharField(max_length=100)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  users = models.ManyToManyField('HwUser', through='HwEducationConnections')
  class Meta:
    db_table = u'hw_education'
    
class HwLanguage(models.Model):
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

class HwLocation(models.Model):
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
  users = models.ManyToManyField('HwUser', through='HwLocationInterests')
  class Meta:
    db_table = u'hw_location'
    
class HwUser(models.Model):
  """Class representing a Hunchworks user."""
  user_id = models.IntegerField(primary_key=True)
  email = models.CharField(max_length=45)
  first_name = models.CharField(max_length=25)
  last_name = models.CharField(max_length=50)
  title = models.IntegerField(
    choices=hunchworks_enums.UserTitle.GetChoices())
  show_profile_reminder = models.IntegerField()
  privacy = models.IntegerField(
    choices=hunchworks_enums.PrivacyLevel.GetChoices())
  username = models.CharField(max_length=20)
  password = models.CharField(max_length=20)
  default_language = models.ForeignKey(HwLanguage)
  bio_text = models.TextField(blank=True)
  phone = models.CharField(max_length=20, blank=True)
  skype_name = models.CharField(max_length=30, blank=True)
  website = models.CharField(max_length=100, blank=True)
  profile_picture = models.CharField(max_length=100, blank=True)
  screen_name = models.CharField(max_length=45, blank=True)
  messenger_service = models.IntegerField(null=True, blank=True)
  skills = models.ManyToManyField('HwSkill', through='HwSkillConnections')
  education = models.ManyToManyField(
  	'HwEducation', through='HwEducationConnections')
  classes = models.ManyToManyField('HwClass', through='HwEducationConnections')
  location_interests = models.ManyToManyField(
  	'HwLocation', through='HwLocationInterests')
  roles = models.ManyToManyField('HwRole', through='HwUserRoles')
  hunches = models.ManyToManyField('HwHunch', through='HwHunchConnections')
  invited_users = models.ManyToManyField(
  	'HwInvitedUser', through='HwUserInvites')
  groups = models.ManyToManyField('HwGroup', through='HwHumanConnections')
  #collaborators = models.ManyToManyField('HwUser', through='HwHumanConnections')
  class Meta:
    db_table = u'hw_user'

class HwEducationConnections(models.Model):
  """Many to Many model representing a user's education and/or classes"""
  education_connection_id = models.IntegerField(primary_key=True)
  user = models.ForeignKey(HwUser)
  education = models.ForeignKey(HwEducation, null=True, blank=True)
  class_field = models.ForeignKey(HwClass, null=True, blank=True)
  class Meta:
    db_table = u'hw_education_connections'
    
class HwHunch(models.Model):
  """Class representing a Hunch."""
  hunch_id = models.IntegerField(primary_key=True)
  creator = models.ForeignKey(HwUser, related_name='%(class)s_creator_id' )
  time_created = models.DateTimeField()
  status = models.IntegerField()
  title = models.CharField(max_length=100)
  privacy = models.IntegerField()
  strength = models.IntegerField()
  language = models.ForeignKey(HwLanguage, null=True, blank=True)
  location = models.ForeignKey(HwLocation, null=True, blank=True)
  description = models.TextField(blank=True)
  skills = models.ManyToManyField('HwSkill', through='HwSkillConnections')
  groups = models.ManyToManyField('HwGroup', through='HwHunchConnections')
  users = models.ManyToManyField('HwUser', through='HwHunchConnections')
  invited_users = models.ManyToManyField(
    'HwInvitedUser', through='HwHunchConnections')
  class Meta:
    db_table = u'hw_hunch'

class HwEvidence(models.Model):
  """Class representing a response to the hunch"""
  evidence_id = models.IntegerField(primary_key=True)
  hunch = models.ForeignKey(HwHunch)
  creator = models.ForeignKey(HwUser)
  strength = models.IntegerField()
  time_created = models.DateTimeField()
  description = models.TextField(blank=True)
  albums = models.ManyToManyField('HwAlbum', through='HwEvidenceAlbums')
  attachments = models.ManyToManyField(
    'HwAttachment', through='HwEvidenceAttachments')
  class Meta:
    db_table = u'hw_evidence'

class HwEvidenceAlbums(models.Model):
  """Many to Many model joining Evidence and Album together"""
  album = models.ForeignKey(HwAlbum)
  evidence = models.ForeignKey(HwEvidence)
  class Meta:
    db_table = u'hw_evidence_albums'

class HwEvidenceAttachments(models.Model):
  """Many to Many model joining evidence and attachments."""
  attachment = models.ForeignKey(HwAttachment)
  evidence = models.ForeignKey(HwEvidence)
  class Meta:
    db_table = u'hw_evidence_attachments'

class HwGroup(models.Model):
  """Class representing a logical grouping of Hunchworks users."""
  group_id = models.IntegerField(primary_key=True)
  name = models.CharField(unique=True, max_length=100, blank=True)
  group_type = models.IntegerField()
  privacy = models.IntegerField()
  location = models.ForeignKey(HwLocation, null=True, blank=True)
  logo = models.CharField(max_length=100, blank=True)
  hunches = models.ManyToManyField('HwHunch', through='HwHunchConnections')
  users = models.ManyToManyField('HwUser', through='HwHumanConnections')
  class Meta:
    db_table = u'hw_group'

class HwHumanConnections(models.Model):
  """Many to Many model joining groups and users with users."""
  human_connection_id = models.IntegerField(primary_key=True)
  user = models.ForeignKey(HwUser, related_name='%(class)s_user_id')
  access_level = models.IntegerField()
  trust_from_user = models.IntegerField()
  trust_from_group = models.IntegerField()
  receive_updates = models.IntegerField()
  status = models.IntegerField()
  group = models.ForeignKey(HwGroup, null=True, blank=True)
  #other_user = models.ForeignKey(HwUser, null=True, blank=True)
  class Meta:
    db_table = u'hw_human_connections'

class HwInvitedUser(models.Model):
  """Class representing a master list of all users ever invited to the system
  and their respective user id's if they created an account."""
  email = models.CharField(max_length=45, primary_key=True)
  user = models.ForeignKey(HwUser, related_name='%(class)s_user_id')
  hunches = models.ManyToManyField('HwHunch', through='HwHunchConnections')
  users = models.ManyToManyField('HwUser', through='HwUserInvites')
  class Meta:
    db_table = u'hw_invited_user'

class HwHunchConnections(models.Model):
  """Many to Many model joining Hunch and User,Group,InvitedUser together"""
  hunch_connection_id = models.IntegerField(primary_key=True)
  hunch = models.ForeignKey(HwHunch)
  status = models.IntegerField()
  user = models.ForeignKey(HwUser, null=True, blank=True)
  group = models.ForeignKey(HwGroup, null=True, blank=True)
  invited_email = models.ForeignKey(HwInvitedUser, null=True, blank=True)
  class Meta:
    db_table = u'hw_hunch_connections'

class HwLocationInterests(models.Model):
  """Many to Many model joining User and Location together for their list
  of locations they are interested in"""
  user = models.ForeignKey(HwUser)
  location = models.ForeignKey(HwLocation)
  class Meta:
    db_table = u'hw_location_interests'

class HwOrganization(models.Model):
  """Class representing an external organization (UNDP etc.)."""
  organization_id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=125)
  abbreviation = models.CharField(max_length=7)
  group = models.ForeignKey(HwGroup)
  location = models.ForeignKey(HwLocation, null=True, blank=True)
  class Meta:
    db_table = u'hw_organization'

class HwRole(models.Model):
  """Class representing a role held by a given user."""
  role_id = models.IntegerField(primary_key=True)
  organization = models.ForeignKey(HwOrganization)
  title = models.CharField(max_length=40)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  description = models.TextField(blank=True)
  users = models.ManyToManyField('HwUser', through='HwUserRoles')
  class Meta:
    db_table = u'hw_role'

class HwSkill(models.Model):
  """Class representing a skill possessed by a user, e.g. HTML."""
  skill_id = models.IntegerField(primary_key=True)
  skill = models.CharField(unique=True, max_length=100)
  is_language = models.IntegerField()
  is_technical = models.IntegerField()
  hunches = models.ManyToManyField('HwHunch', through='HwSkillConnections')
  users = models.ManyToManyField('HwUser', through='HwSkillConnections')
  class Meta:
    db_table = u'hw_skill'

class HwSkillConnections(models.Model):
  """Many to Many model joining hunches, user and skills.

  This model represents the skill-set required to progress a hunch and the skill
  level needed for each skill. It also has the skillset of a user, and the level
  for each skill. 
  """
  skill_connection_id = models.IntegerField(primary_key=True)
  skill = models.ForeignKey(HwSkill)
  level = models.IntegerField()
  hunch = models.ForeignKey(HwHunch, null=True, blank=True)
  user = models.ForeignKey(HwUser, null=True, blank=True)
  class Meta:
    db_table = u'hw_skill_connections'

class HwUserInvites(models.Model):
  """Many to Many model joining User and Invited User together for the users 
  invited people list"""
  user = models.ForeignKey(HwUser)
  invited_email = models.ForeignKey(HwInvitedUser)
  status = models.IntegerField()
  class Meta:
    db_table = u'hw_user_invites'

class HwUserRoles(models.Model):
  """Many To many model representing a user's roles or positions."""
  user = models.ForeignKey(HwUser)
  role = models.ForeignKey(HwRole)
  class Meta:
    db_table = u'hw_user_roles'

# Getters for setting the default values for ForeignKeys on other models.
def GetDefaultLanguage():
  return Language.objects.get(pk='en')


def GetHunchGroup():
  # TODO(leah): Set this up to auto-create a new group, taking names, owners
  #       etc. from the hunch. Need to figure out how to pass that stuff
  #       in.
  pass
