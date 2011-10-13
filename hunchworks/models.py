#!/usr/bin/env python

import datetime
from urlparse import urlparse
import hunchworks_enums
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save


PRIVACY_CHOICES = (
  (0, "Hidden"),
  (1, "Closed"),
  (2, "Open"))

PRIVACY_HELP_TEXT = "<br>".join([
  "<strong>Hidden</strong>: only visible to invited members.",
  "<strong>Closed</strong>: visible to everyone, but only invited members can participate.",
  "<strong>Open</strong>: available to any HunchWorks member."])

GROUP_STATUS_CHOICES = (
  (0, "Invited"),
  (1, "Accepted"),
  (2, "Blocked"))

SUPPORT_CHOICES = (
  (-2, "Strongly Refutes"),
  (-1, "Mildly Refutes"),
  (0, "Neutral"),
  (1, "Midly Supports"),
  (2, "Strongly Supports"))


class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  title = models.IntegerField(choices=hunchworks_enums.UserTitle.GetChoices(), default=0)
  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=75)
  privacy = models.IntegerField(choices=hunchworks_enums.PrivacyLevel.GetChoices(), default=0)
  bio_text = models.TextField(blank=True)
  phone = models.CharField(max_length=20, blank=True)
  skype_name = models.CharField(max_length=30, blank=True)
  website = models.CharField(max_length=100, blank=True)
  profile_picture = models.ImageField(upload_to="profile_images", blank=True)
  messenger_service = models.IntegerField(null=True, blank=True, choices=hunchworks_enums.MessangerServices.GetChoices(), default=0)
  translation_language = models.ForeignKey('TranslationLanguage', default=0)

  invitation = models.ForeignKey('Invitation', unique=True, null=True, blank=True)
  connections = models.ManyToManyField('self', through='Connection', symmetrical=False, blank=True)

  roles = models.ManyToManyField("Role", blank=True)
  location_interests = models.ManyToManyField('Location', blank=True)
  skills = models.ManyToManyField('Skill', blank=True)
  languages = models.ManyToManyField('Language', blank=True)

  qualifications = models.ManyToManyField('Education', blank=True)
  courses = models.ManyToManyField('Course', blank=True)

  def __unicode__(self):
    return self.user.username

  @models.permalink
  def get_absolute_url(self):
    return ("profile", [self.pk])

  def profile_picture_url(self):
    return "http://icanhascheezburger.files.wordpress.com/2011/09/funny-pictures-oh-like-you-trying-to-squeeze-your-fat-ass-into-a-leopard-print-thong-is-any-different.jpg"


def create_user(sender, instance, created, **kwargs):
  if created: UserProfile.objects.create(user=instance)

post_save.connect(create_user, sender=User)


class Connection(models.Model):
  user_profile       = models.ForeignKey('UserProfile', related_name="outgoing_connections")
  other_user_profile = models.ForeignKey('UserProfile', related_name="incoming_connections")
  status             = models.IntegerField(default=0)

  def __unicode__(self):
    return "%s -> %s" % (self.user_profile, self.other_user_profile)

  @classmethod
  def search(cls, term, user_profile=None):
    return cls.objects.filter(user_profile=user_profile, other_user_profile__user__username__icontains=term)


class Hunch(models.Model):
  creator = models.ForeignKey('UserProfile', related_name="created_hunches")
  time_created = models.DateTimeField()
  time_modified = models.DateTimeField()
  status = models.IntegerField(choices=hunchworks_enums.HunchStatus.GetChoices(), default=2)
  title = models.CharField(max_length=100, unique=True)
  privacy = models.IntegerField(choices=PRIVACY_CHOICES, default=0, help_text=PRIVACY_HELP_TEXT)
  translation_language = models.ForeignKey('TranslationLanguage', default=0)
  location = models.ForeignKey('Location', null=True, blank=True)
  description = models.TextField()

  skills = models.ManyToManyField('Skill', blank=True)
  languages = models.ManyToManyField('Language', blank=True)
  evidences = models.ManyToManyField('Evidence', through='HunchEvidence', blank=True)
  tags = models.ManyToManyField('Tag', blank=True)
  user_profiles = models.ManyToManyField('UserProfile', through='HunchUser')

  class Meta:
    verbose_name_plural = "hunches"

  def __unicode__(self):
    return self.title

  @models.permalink
  def get_absolute_url(self):
    return ("hunch", [self.pk])

  def save(self, *args, **kwargs):
    now = datetime.datetime.today()

    # for new records.
    if not self.id:
      self.time_created = now

    self.time_modified = now
    super(Hunch, self).save(*args, **kwargs)

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

  def evidences_for(self):
    return HunchEvidence.objects.filter(hunch=self, support_cache__gt=0).order_by("-confidence_cache")

  def evidences_against(self):
    return HunchEvidence.objects.filter(hunch=self, support_cache__lte=0).order_by("-confidence_cache")

  def _is_hidden(self):
    """Return True if this Hunch is hidden."""
    return (self.privacy == hunchworks_enums.PrivacyLevel.HIDDEN)

  def member_count(self):
    return self.user_profiles.all().count()

  def evidence_count(self):
    return self.evidences.all().count()


class HunchUser(models.Model):
  hunch = models.ForeignKey('Hunch')
  user_profile = models.ForeignKey('UserProfile')
  status = models.IntegerField(default=0)


class Evidence(models.Model):
  title = models.CharField(max_length=100, blank=True)
  time_created = models.DateTimeField()
  time_modified = models.DateTimeField()
  description = models.TextField(blank=True)
  creator = models.ForeignKey('UserProfile')
  link = models.CharField(max_length=255)
  tags = models.ManyToManyField('Tag', blank=True)

  def __unicode__(self):
    return self.title or self.description

  def type(self):
    return "Link"

  def short_link(self, max_length=32):
    return urlparse(self.link).hostname

  def save(self, *args, **kwargs):
    now = datetime.datetime.today()

    # for new records.
    if not self.id:
      self.time_created = now

    self.time_modified = now
    super(Evidence, self).save(*args, **kwargs)

  @models.permalink
  def get_absolute_url(self):
    return ("evidence", [self.pk])

  @classmethod
  def search(cls, term, user_profile=None):
    return cls.objects.filter(description__icontains=term)


class Group(models.Model):
  name = models.CharField(max_length=100, unique=True)
  abbreviation = models.CharField(max_length=10, null=True, blank=True)
  description = models.TextField(blank=True, help_text="You can use HTML here.")
  logo = models.CharField(max_length=100, blank=True, null=True) # TODO filefield
  type = models.IntegerField(choices=hunchworks_enums.GroupType.GetChoices(), default=0)
  privacy = models.IntegerField(choices=PRIVACY_CHOICES, default=0, help_text=PRIVACY_HELP_TEXT)
  location = models.ForeignKey('Location', null=True, blank=True)
  members = models.ManyToManyField('UserProfile', through='UserProfileGroup', null=True, blank=True)

  def __unicode__(self):
    return self.name

  @models.permalink
  def get_absolute_url(self):
    return ("group", [self.pk])

  def logo_url(self):
    return "http://i.imgur.com/BYf54.jpg"

  def member_count(self):
    return self.members.all().count()

  def hunch_count(self):
    return 0


class UserProfileGroup(models.Model):
  user_profile = models.ForeignKey('UserProfile')
  group = models.ForeignKey('Group')
  status = models.IntegerField(choices=GROUP_STATUS_CHOICES, default=0)

  def __unicode__(self):
    return "<UserProfileGroup:%d>" % self.pk


class Attachment(models.Model):
  type = models.IntegerField()
  file_location = models.CharField(max_length=100) # TODO filefield

  def __unicode__(self):
    return "<Attachment:%d>" % self.pk


class Album(models.Model):
  name = models.CharField(max_length=45)
  evidences = models.ManyToManyField('Evidence')

  def __unicode__(self):
    return self.name
    
  @models.permalink
  def get_absolute_url(self):
    return ("album", [self.pk])


class Education(models.Model):
  school = models.CharField(max_length=255)
  qualification = models.CharField(max_length=100)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)

  def __unicode__(self):
    return "<Education:%d>" % self.pk


class Course(models.Model):
  """
  An more informal educational course which does not fit neatly into the
  Education model. (E.g. "Diploma from NYC underwater welding club".)
  """

  name = models.CharField(max_length=45)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)

  class Meta:
    verbose_name_plural = "classes"

  def __unicode__(self):
    return "<Course:%d>" % self.pk


class TranslationLanguage(models.Model):
  name = models.CharField(unique=True, max_length=45)

  def __unicode__(self):
    return self.name


class Location(models.Model):
  latitude = models.DecimalField(max_digits=9, decimal_places=6)
  longitude = models.DecimalField(max_digits=9, decimal_places=6)
  name = models.CharField(max_length=200, blank=True)

  def __unicode__(self):
    return self.name or "<Location:%d>" % self.pk
  
  @classmethod
  def search(cls, term, user_profile=None):
    return cls.objects.filter(name__icontains=term)


class Tag(models.Model):
  name = models.CharField(max_length=40)

  def __unicode__(self):
    return self.name

  @classmethod
  def search(cls, term, user_profile=None):
    return cls.objects.filter(name__icontains=term)


class Role(models.Model):
  group = models.ForeignKey('Group')
  title = models.CharField(max_length=40)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  description = models.TextField(blank=True)

  def __unicode__(self):
    return self.title


class Skill(models.Model):
  name = models.CharField(unique=True, max_length=100)

  def __unicode__(self):
    return self.name

  @classmethod
  def search(cls, term, user_profile=None):
    return cls.objects.filter(name__icontains=term)


class Language(models.Model):
  name = models.CharField(unique=True, max_length=100)

  def __unicode__(self):
    return self.name

  @classmethod
  def search(cls, term, user_profile=None):
    return cls.objects.filter(name__icontains=term)


class Invitation(models.Model):
  email = models.CharField(max_length=100)
  invited_by = models.ForeignKey('UserProfile', related_name="invitations")
  hunch = models.ForeignKey('Hunch', null=True, blank=True)

  def __unicode__(self):
    return "%s to %s" % (self.email, self.hunch)


class Comment(models.Model):
  creator        = models.ForeignKey('UserProfile')
  time_posted    = models.DateTimeField()
  text           = models.TextField()
  hunch          = models.ForeignKey('Hunch', null=True, blank=True)
  hunch_evidence = models.ForeignKey('HunchEvidence', null=True, blank=True)

  @models.permalink
  def get_absolute_base_url(self):
    if self.hunch_evidence:
      return ("hunch", [self.hunch_evidence.hunch.pk])

  def get_absolute_url(self):
    return self.get_absolute_base_url() + ("#c%d" % self.pk)

  def save(self, *args, **kwargs):
    self.time_posted = datetime.datetime.today()
    super(Comment, self).save(*args, **kwargs)


class HunchEvidence(models.Model):
  hunch = models.ForeignKey('Hunch')
  evidence = models.ForeignKey('Evidence')
  support_cache = models.IntegerField(choices=SUPPORT_CHOICES)
  confidence_cache = models.FloatField()

  def save(self, *args, **kwargs):
    self.support_cache = 0
    self.confidence_cache = 0.5
    super(HunchEvidence, self).save(*args, **kwargs)
