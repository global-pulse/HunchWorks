#!/usr/bin/env python

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

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

import datetime

# Enums used throughout Hunchworks.
import hunchworks_enums

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class HwAlbum(models.Model):
  """Class representing a collection of pictures in an album"""
  album_id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=45)
  class Meta:
    db_table = u'hw_album'
    
class HwAttachment(models.Model):
  """Class representing an attachment for a hunch"""
  attachment_id = models.AutoField(primary_key=True)
  attachment_type = models.IntegerField()
  file_location = models.CharField(max_length=100)
  albums = models.ManyToManyField('HwAlbum', through='HwAlbumAttachments')
  class Meta:
    db_table = u'hw_attachment'
    
class HwAlbumAttachments(models.Model):
  """Many to Many model joining Album and attachments"""
  album_attachment_id = models.AutoField(primary_key=True)
  album = models.ForeignKey(HwAlbum)
  attachment = models.ForeignKey(HwAttachment)
  class Meta:
    db_table = u'hw_album_attachments'

class HwClass(models.Model):
  """Class representing a educational class taken that may or may not have
  been at a college"""
  class_id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=45)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  class Meta:
    db_table = u'hw_class'
    
class HwEducation(models.Model):
  """Class representing a degree or qualification obtained by a user."""
  education_id = models.AutoField(primary_key=True)
  school = models.CharField(max_length=255)
  qualification = models.CharField(max_length=100)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
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
  language_id = models.AutoField(primary_key=True, default=0)
  language_name = models.CharField(unique=True, max_length=45)
  class Meta:
    db_table = u'hw_language'

  def __unicode__(self):
    return self.language_name


class HwLocation(models.Model):
  """Class representing a location used by the application.

  These locations are derived from either:
  1. Open Street Map Nominatim API (
     http://wiki.openstreetmap.org/wiki/Nominatim)
  2. Google Maps Geocoding API (
     http://code.google.com/apis/maps/documentation/geocoding/#JSON)

  That decision is still TBD, so for now this class is a stub.
  """
  location_id = models.AutoField(primary_key=True)
  location_name = models.CharField(unique=True, max_length=45)
  class Meta:
    db_table = u'hw_location'
    
  def __unicode__(self):
    return self.location_name
    
class HwUser(models.Model):
  """Extend HwUser from User"""
  user = models.ForeignKey(User, unique=True, primary_key=True)
  """Class representing a Hunchworks user."""
  title = models.IntegerField(
    choices=hunchworks_enums.UserTitle.GetChoices(), default=0)
  show_profile_reminder = models.IntegerField(default=0)
  privacy = models.IntegerField(
    choices=hunchworks_enums.PrivacyLevel.GetChoices(), default=0)
  bio_text = models.TextField(blank=True)
  phone = models.CharField(max_length=20, blank=True)
  skype_name = models.CharField(max_length=30, blank=True)
  website = models.CharField(max_length=100, blank=True)
  profile_picture = models.CharField(max_length=100, blank=True)
  screen_name = models.CharField(max_length=45, blank=True)
  messenger_service = models.IntegerField(null=True, blank=True, 
    choices=hunchworks_enums.MessangerServices.GetChoices(), default=0)
  default_language = models.ForeignKey(HwLanguage, default=0)
  skills = models.ManyToManyField('HwSkill', through='HwSkillConnections', blank=True)
  education = models.ManyToManyField(
  	'HwEducation', through='HwEducationConnections')
  classes = models.ManyToManyField('HwClass', through='HwEducationConnections')
  location_interests = models.ManyToManyField(
  	'HwLocation', through='HwLocationInterests')
  roles = models.ManyToManyField('HwRole', through='HwUserRoles')
  hunches = models.ManyToManyField('HwHunch', through='HwHunchConnections')
  groups = models.ManyToManyField('HwGroup', through='HwGroupConnections', blank=True)
  collaborators = models.ManyToManyField('self', through='HwUserConnections', blank=True, symmetrical=False)
  class Meta:
    db_table = u'hw_user'

  #def __unicode__(self):
  #  return self.username

class HwEducationConnections(models.Model):
  """Many to Many model representing a user's education and/or classes"""
  education_connection_id = models.AutoField(primary_key=True)
  user = models.ForeignKey(HwUser)
  education = models.ForeignKey(HwEducation, null=True, blank=True)
  class_field = models.ForeignKey(HwClass, null=True, blank=True)
  class Meta:
    db_table = u'hw_education_connections'


class HwHunch(models.Model):
  """Class representing a Hunch."""
  hunch_id = models.AutoField(primary_key=True)
  creator = models.ForeignKey(HwUser, related_name='%(class)s_creator_id' )
  time_created = models.DateTimeField()
  time_modified = models.DateTimeField()
  status = models.IntegerField(choices=hunchworks_enums.HunchStatus.GetChoices(), default=2)
  title = models.CharField(max_length=100)
  privacy = models.IntegerField(choices=hunchworks_enums.PrivacyLevel.GetChoices(), default=0)
  hunch_strength = models.IntegerField(default=0)
  language = models.ForeignKey(HwLanguage)
  location = models.ForeignKey(HwLocation, null=True, blank=True)
  hunch_description = models.TextField()
  skills = models.ManyToManyField('HwSkill', through='HwSkillConnections')
  hunch_tags = models.ManyToManyField('HwTag', through='HwTagConnections', blank=True)
  invited_users = models.ManyToManyField(
    'HwInvitedUser', through='HwHunchConnections')

  class Meta:
    db_table = u'hw_hunch'

  def save(self, *args, **kwargs):
    now = datetime.datetime.today()

    # for new records.
    if not self.hunch_id:
      self.time_created = now

    self.time_modified = now
    super(HwHunch, self).save(*args, **kwargs)

  def is_editable_by(self, user):
    """Return True if this Hunch is editable by `user` (a Django auth user)."""
    return (self.creator.user == user)

  def is_viewable_by(self, user):
    """Return True if this Hunch is viewable by `user` (a Django auth user)."""

    if self._is_hidden():
      return (self.creator.user == user)

    # Otherwise, if the hunch is OPEN or CLOSED, anyone (even anonymous) can
    # view it. The only distinction between the levels is in the editing.
    return True

  def _is_hidden(self):
    """Return True if this Hunch is hidden."""
    return (self.privacy == hunchworks_enums.PrivacyLevel.HIDDEN)

class HwEvidence(models.Model):
  """Class representing a response to the hunch"""
  evidence_id = models.AutoField(primary_key=True)
  evidence_strength = models.IntegerField(default=0)
  time_created = models.DateTimeField()
  time_modified = models.DateTimeField()
  evidence_description = models.TextField(blank=True)
  hunch = models.ForeignKey(HwHunch)
  creator = models.ForeignKey(HwUser)
  albums = models.ManyToManyField('HwAlbum', through='HwEvidenceAlbums')
  attachments = models.ManyToManyField(
    'HwAttachment', through='HwEvidenceAttachments')
  evidence_tags = models.ManyToManyField('HwTag', through='HwTagConnections')
  class Meta:
    db_table = u'hw_evidence'
    
  def save(self, *args, **kwargs):
    now = datetime.datetime.today()

    # for new records.
    if not self.evidence_id:
      self.time_created = now

    self.time_modified = now
    super(HwEvidence, self).save(*args, **kwargs)

class HwEvidenceAlbums(models.Model):
  """Many to Many model joining Evidence and Album together"""
  evidence_album_id = models.AutoField(primary_key=True)
  album = models.ForeignKey(HwAlbum)
  evidence = models.ForeignKey(HwEvidence)
  class Meta:
    db_table = u'hw_evidence_albums'

class HwEvidenceAttachments(models.Model):
  """Many to Many model joining evidence and attachments."""
  evidence_album_id = models.AutoField(primary_key=True)
  attachment = models.ForeignKey(HwAttachment)
  evidence = models.ForeignKey(HwEvidence)
  class Meta:
    db_table = u'hw_evidence_attachments'

class HwGroup(models.Model):
  """Class representing a logical grouping of Hunchworks users."""
  group_id = models.AutoField(primary_key=True)
  name = models.CharField(unique=True, max_length=100, blank=True)
  group_type = models.IntegerField(choices=hunchworks_enums.GroupType.GetChoices(), default=0)
  privacy = models.IntegerField(choices=hunchworks_enums.PrivacyLevel.GetChoices(), default=0)
  logo = models.CharField(max_length=100, blank=True)
  location = models.ForeignKey(HwLocation, null=True, blank=True)
  class Meta:
    db_table = u'hw_group'

class HwGroupConnections(models.Model):
  """Many to Many model joining groups and users with users."""
  group_connection_id = models.AutoField(primary_key=True)
  access_level = models.IntegerField()
  status = models.IntegerField()
  user = models.ForeignKey(HwUser, related_name='%(class)s_user_id')
  group = models.ForeignKey(HwGroup)
  class Meta:
    db_table = u'hw_human_connections'

class HwInvitedUser(models.Model):
  """Class representing a master list of all users ever invited to the system
  and their respective user id's if they created an account."""
  invited_user = models.AutoField(primary_key=True)
  email = models.CharField(max_length=45)
  status = models.IntegerField()
  created_user = models.ForeignKey(HwUser, related_name='created_user_id',
    blank=True)
  invited_by = models.ForeignKey(HwUser, related_name='invited_by_id')
    
  class Meta:
    db_table = u'hw_invited_user'

class HwHunchConnections(models.Model):
  """Many to Many model joining Hunch and User,Group,InvitedUser together"""
  hunch_connection_id = models.AutoField(primary_key=True)
  status = models.IntegerField()
  hunch = models.ForeignKey(HwHunch)
  user = models.ForeignKey(HwUser, null=True, blank=True)
  invited_email = models.ForeignKey(HwInvitedUser, null=True, blank=True)
  class Meta:
    db_table = u'hw_hunch_connections'

class HwLocationInterests(models.Model):
  """Many to Many model joining User and Location together for their list
  of locations they are interested in"""
  location_interest_id = models.AutoField(primary_key=True)
  user = models.ForeignKey(HwUser)
  location = models.ForeignKey(HwLocation)
  class Meta:
    db_table = u'hw_location_interests'

class HwOrganization(models.Model):
  """Class representing an external organization (UNDP etc.)."""
  organization_id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=125)
  abbreviation = models.CharField(max_length=7)
  group = models.ForeignKey(HwGroup)
  location = models.ForeignKey(HwLocation, null=True, blank=True)
  class Meta:
    db_table = u'hw_organization'

class HwRole(models.Model):
  """Class representing a role held by a given user."""
  role_id = models.AutoField(primary_key=True)
  organization = models.ForeignKey(HwOrganization)
  title = models.CharField(max_length=40)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  description = models.TextField(blank=True)
  class Meta:
    db_table = u'hw_role'

class HwSkill(models.Model):
  """Class representing a skill possessed by a user, e.g. HTML."""
  skill_id = models.AutoField(primary_key=True)
  skill_name = models.CharField(unique=True, max_length=100)
  is_language = models.IntegerField()
  is_technical = models.IntegerField()

  class Meta:
    db_table = u'hw_skill'

  def __unicode__(self):
    return self.skill_name

class HwSkillConnections(models.Model):
  """Many to Many model joining hunches, user and skills.

  This model represents the skill-set required to progress a hunch and the 
  skill level needed for each skill. It also has the skillset of a user, and 
  the level for each skill. 
  """
  skill_connection_id = models.AutoField(primary_key=True)
  skill = models.ForeignKey(HwSkill)
  level = models.IntegerField()
  hunch = models.ForeignKey(HwHunch, null=True, blank=True)
  user = models.ForeignKey(HwUser, null=True, blank=True)
  class Meta:
    db_table = u'hw_skill_connections'

  #def __unicode__(self):
  #  return str(self.skill.skill_id)

class HwUserRoles(models.Model):
  """Many To many model representing a user's roles or positions."""
  user_role_id = models.AutoField(primary_key=True)
  user = models.ForeignKey(HwUser)
  role = models.ForeignKey(HwRole)
  class Meta:
    db_table = u'hw_user_roles'

class HwTag(models.Model):
  """Class representing tags you can add to Evidence and Hunches for searching
  easability"""
  tag_id = models.AutoField(primary_key=True)
  tag_name = models.CharField(max_length=40)
  class Meta:
    db_table = u'hw_tag'

class HwTagConnections(models.Model):
  """Many to Many connector for Hunch, Evidence, and Tag classes"""
  tag_connection_id = models.AutoField(primary_key=True)
  tag = models.ForeignKey(HwTag)
  hunch = models.ForeignKey(HwHunch, blank=True, null=True)
  evidence = models.ForeignKey(HwEvidence, blank=True, null=True)
  class Meta:
    db_table = u'hw_tag_connections'

class HwUserConnections(models.Model):
  """Class representing a many to many relationship between users"""
  user_connection_id = models.AutoField(primary_key=True)
  status = models.IntegerField()
  user = models.ForeignKey(HwUser, related_name='conn_user_id')
  other_user = models.ForeignKey(HwUser, related_name='other_user_id')
  class Meta:
    db_table = u'hw_user_connections'
  

# Getters for setting the default values for ForeignKeys on other models.
def GetDefaultLanguage():
  return Language.objects.get(pk='en')


def GetHunchGroup():
  # TODO(leah): Set this up to auto-create a new group, taking names, owners
  #       etc. from the hunch. Need to figure out how to pass that stuff
  #       in.
  pass

def create_hw_user(sender, instance, created, **kwargs):
    if created:
        HwUser.objects.create(user=instance)

post_save.connect(create_hw_user, sender=User)

