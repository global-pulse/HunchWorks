#!/usr/bin/env python

import datetime
import numpy
from urlparse import urlparse
import hunchworks_enums
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.template import Template, Context
from django.db.models.signals import pre_save, post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


PRIVACY_CHOICES = (
  (0, "Hidden"),
  (1, "Closed"),
  (2, "Open"))

PRIVACY_HELP_TEXT = "<br>".join([
  "<strong>Hidden</strong>: only visible to explicitly invited users.",
  "<strong>Closed</strong>: visible to all, but only invited users can contribute.",
  "<strong>Open</strong>: available to any HunchWorks user."])

GROUP_STATUS_CHOICES = (
  (0, "Invited"),
  (1, "Accepted"),
  (2, "Blocked"))

SUPPORT_CHOICES = (
  (-2, "Strongly Refutes"),
  (-1, "Mildly Refutes"),
  (0, "Neutral"),
  (1, "Mildly Supports"),
  (2, "Strongly Supports"))

_support_values = zip(*SUPPORT_CHOICES)[0]
MIN_SUPPORT = min(_support_values)
MAX_SUPPORT = max(_support_values)

# The maximum possible standard deviation of a set of SUPPORT_CHOICES, for
# calculating the controversy ratio of a Hunch or HunchEvidence.
SUPPORT_MAX_DEVIATION = numpy.std([MIN_SUPPORT, MAX_SUPPORT])


POS_INF = float("inf")
NEG_INF = float("-inf")

SUPPORT_RANGES = (
  (0, 0,          "Neutral",            "This hunch is not conclusively supported nor refuted by evidence."),
  (1.1, POS_INF,  "Strongly Supported", "This hunch is strongly supported by evidence, with {{ confidence }} confidence."),
  (NEG_INF, -1.1, "Strongly Refuted",   "This hunch is strongly refuted by evidence, with {{ confidence }} confidence."),
  (0, 1.1,        "Mildly Supported",   "This hunch is supported by evidence, but only with {{ confidence }} confidence."),
  (-1.1, 0,       "Mildly Refuted",     "This hunch is refuted by evidence, but only with {{ confidence }} confidence."))

CONTROVERSY_RANGES = (
  (0, 0.2,        "Uncontroversial",        "This hunch is not controversial within the HunchWorks community."),
  (0.2, 0.6,      "Somewhat Controversial", "Some members of the HunchWorks community dispute this hunch."),
  (0.6, 0.95,     "Controversial",          "Many members of the HunchWorks community dispute this hunch."),
  (0.95, POS_INF, "Very Controversial",     "This hunch is widely disputed within the HunchWorks community."))

# (days_to_consider, minimum_activity, text, verbose_text)
ACTIVITY_RANGES = (
  (1, 2,    "Very Active", "This hunch is being discussed by the HunchWorks community today."),
  (7, 1,    "Active",      "This hunch is has been discussed by the HunchWorks community within a week."),
  (None, 0, "Inactive",    "This hunch is not being discussed or evaluated by the HunchWorks community."))


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
  profile_picture = models.ImageField(upload_to="profile_images", blank=True, null=True)
  messenger_service = models.IntegerField(null=True, blank=True, choices=hunchworks_enums.MessangerServices.GetChoices(), default=0)
  translation_language = models.ForeignKey('TranslationLanguage', default=0)

  invitation = models.ForeignKey('Invitation', unique=True, null=True, blank=True)
  connections = models.ManyToManyField('self', through='Connection', symmetrical=False, blank=True)

  roles = models.ManyToManyField("Role", blank=True)
  location_interests = models.ManyToManyField('Location', blank=True)

  qualifications = models.ManyToManyField('Education', blank=True)
  courses = models.ManyToManyField('Course', blank=True)

  def __unicode__(self):
    return self.name or self.user.username

  @models.permalink
  def get_absolute_url(self):
    return ("profile", [self.pk])

  def profile_picture_url(self):
    if self.profile_picture:
      return self.profile_picture.url
    else:
      return "http://www.clker.com/cliparts/5/9/4/c/12198090531909861341man%20silhouette.svg.hi.png"


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

  title = models.CharField(max_length=160)
  description = models.TextField(blank=True)

  privacy = models.IntegerField(choices=PRIVACY_CHOICES, default=0, help_text=PRIVACY_HELP_TEXT)
  location = models.ForeignKey('Location', null=True, blank=True)
  evidences = models.ManyToManyField( 'Evidence', through='HunchEvidence', blank=True)
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


  def get_support(self):
    supports = map(HunchEvidence.get_support, self.hunchevidence_set.all())
    return (sum(supports) / len(supports)) if any(supports) else 0

  def get_support_range(self):
    s = self.get_support()

    for min_val, max_val, text, desc in SUPPORT_RANGES:
      if (min_val <= s) and (max_val >= s):
        return (text, desc)

    return ("Unknown", "The support level of this hunch cannot be determined.")

  def get_support_text(self):
    return self.get_support_range()[0]

  def get_verbose_support_text(self):
    tmpl = self.get_support_range()[1]
    return Template(tmpl).render(Context({
      "confidence": self.get_confidence_text()
    }))


  def get_confidence(self):
    return abs(self.get_support()) / MAX_SUPPORT

  def get_confidence_text(self):
    return unicode(int(round(self.get_confidence() * 100))) + "%"


  def get_controversy(self):
    choices = Vote.objects.filter(hunch_evidence__hunch=self).values_list("choice", flat=True)
    return (numpy.std(choices) / SUPPORT_MAX_DEVIATION) if any(choices) else 0

  def get_controversy_range(self):
    s = self.get_controversy()

    for min_val, max_val, text, desc in CONTROVERSY_RANGES:
      if (min_val <= s) and (max_val >= s):
        return (text, desc)

    return ("Unknown", "The controversy level of this hunch cannot be determined.")

  def get_controversy_text(self):
    return self.get_controversy_range()[0]

  def get_verbose_controversy_text(self):
    return self.get_controversy_range()[1]


  def activity_count(self, since_days=7):
    since = datetime.datetime.now() -\
      datetime.timedelta(days=since_days)

    votes = Vote.objects.filter(
      hunch_evidence__hunch=self,
      time_updated__gt=since)

    comments = Comment.objects.filter(
      hunch_evidence__hunch=self,
      time_posted__gt=since)

    return votes.count() + comments.count()

  def get_activity_range(self):
    for days, min_activity, text, desc in ACTIVITY_RANGES:
      if (days is None) or (self.activity_count(days) >= min_activity):
        return (text, desc)

    return ("Unknown", "The activity level of this hunch cannot be determined.")

  def get_activity_text(self):
    return self.get_activity_range()[0]

  def get_verbose_activity_text(self):
    return self.get_activity_range()[1]


  @property
  def privacy_text(self):
    return self.get_privacy_display()

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
  title = models.CharField(verbose_name="Short description", max_length=100, blank=True,
    help_text="This should be a short summary of the evidence or what it contains")
  time_created = models.DateTimeField()
  time_modified = models.DateTimeField()
  description = models.TextField(verbose_name="Further explanation", blank=True)
  location = models.ForeignKey('Location', null=True, blank=True)
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
    return cls.objects.filter(
      Q(description__icontains=term) | Q(title__icontains=term))


class Group(models.Model):
  name = models.CharField(max_length=100, unique=True)
  abbreviation = models.CharField(max_length=10, null=True, blank=True)
  description = models.TextField(blank=True, help_text="You can use HTML here.")
  logo = models.ImageField(verbose_name="Group picture", upload_to="group_images", blank=True, null=True)
  type = models.IntegerField(choices=hunchworks_enums.GroupType.GetChoices(), default=0)
  privacy = models.IntegerField(choices=PRIVACY_CHOICES, default=0, help_text=PRIVACY_HELP_TEXT)
  location = models.ForeignKey('Location', null=True, blank=True,
    help_text="The location in the world where the group is located")
  members = models.ManyToManyField('UserProfile', through='UserProfileGroup', null=True, blank=True)

  def __unicode__(self):
    return self.name

  @models.permalink
  def get_absolute_url(self):
    return ("group", [self.pk])

  def logo_url(self):
    if self.logo:
      return self.logo.url
    else:
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
  support_cache = models.IntegerField(choices=SUPPORT_CHOICES, null=True)
  confidence_cache = models.FloatField(null=True)

  class Meta:
    unique_together = ("hunch", "evidence")

  def save(self, *args, **kwargs):
    self.support_cache = self.get_support()
    self.confidence_cache = self.get_controversy()
    super(HunchEvidence, self).save(*args, **kwargs)

  def get_support(self):
    return self.vote_set.aggregate(models.Avg("choice"))["choice__avg"] or 0

  def get_controversy(self):
    choices = self.vote_set.values_list("choice", flat=True)

    if len(choices):
      return numpy.std(choices) / SUPPORT_MAX_DEVIATION

    else:
      return 0


class Vote(models.Model):
  choice = models.IntegerField(choices=SUPPORT_CHOICES, default=None)
  hunch_evidence = models.ForeignKey('HunchEvidence')
  user_profile = models.ForeignKey('UserProfile')
  time_updated = models.DateTimeField()

  def save(self, *args, **kwargs):
    self.time_updated = datetime.datetime.now()
    return super(Vote, self).save(*args, **kwargs)


def update_hunch_evidence_caches(sender, instance, created, **kwargs):
  instance.hunch_evidence.save()

post_save.connect(
  update_hunch_evidence_caches,
  sender=Vote)


class Bookmark(models.Model):
  user_profile = models.ForeignKey('UserProfile')
  
  #Generic foreign key
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey('content_type', 'object_id')

  @classmethod
  def bookmark_get_create(cls, object, user_profile):
    try:
      object_type = ContentType.objects.get_for_model(object)
      bookmark = cls.objects.get(content_type=object_type.id, object_id=object.id, user_profile=user_profile)
      return bookmark
    except cls.DoesNotExist:
      bookmark = cls.objects.create(content_object=object, user_profile=user_profile)
      return bookmark
