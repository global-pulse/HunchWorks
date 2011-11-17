#!/usr/bin/env python

from django import forms
from django.db import transaction
from hunchworks import models
from hunchworks import json_views
from hunchworks.forms.evidence import EvidenceForm
from hunchworks.fields import TokenField, EmbedField, LocationField, EvidencesField


class HunchFormOne(forms.Form):
  title = forms.CharField(label="Hypothesis", max_length=160, required=True,
    help_text='Hypotheses should be a simple <a href="http://en.wikipedia.org/wiki/Falsifiability">falsifiable</a> statement.')

  description = forms.CharField(label="Further Explanation", widget=forms.Textarea, required=False,
    help_text="")

  privacy = forms.ChoiceField(choices=models.PRIVACY_CHOICES,
    help_text=models.PRIVACY_HELP_TEXT)


class HunchFormTwo(EvidenceForm):
  evidences = EvidencesField(required=False,
    label="Attach Existing Evidence")

  link = EmbedField(required=False,
    help_text='Enter an URL to be embedded. You can find a list of supported ' +
              'providers at <a href="http://embed.ly/providers">Embedly</a>.')


class HunchFormThree(forms.Form):
  tags = TokenField(models.Tag, json_views.tags, required=False,
    help_text="Tags should include keywords related to this hunch, to help other users find it.")

  location = LocationField(required=False,
    help_text="If the hunch is relative to a specific location, you can mark it here.")

  user_profiles = TokenField(models.UserProfile, json_views.collaborators, required=False,
    help_text="Type the name of the user you would like to invite to work with you on this hunch",
    label="Invite your connections")

  add_groups = TokenField(models.Group, json_views.user_groups, required=False,
    help_text="Type the name of the group you would like to invite",
    label="Invite your groups")


class HunchForm(forms.ModelForm):
  tags = TokenField(models.Tag, json_views.tags, required=False,
    help_text="Tags should include keywords related to this hunch, to help other users find it.")

  user_profiles = TokenField(models.UserProfile, json_views.collaborators, required=False,
    help_text="Type the name of the user you would like to invite to work with you on this hunch",
    label="Invite your connections")

  add_groups = TokenField(models.Group, json_views.user_groups, required=False,
    help_text="Type the name of the group you would like to invite",
    label="Invite your groups")

  location = LocationField(required=False,
    help_text="If the hunch is relative to a specific location, you can mark it here.")

  evidences = EvidencesField(required=False,
    label="Attach Existing Evidence")

  class Meta:
    model = models.Hunch
    exclude = (
      "creator", "time_created", "time_modified",
    )

  def __init__(self, *args, **kwargs):
    super(HunchForm, self).__init__(*args, **kwargs)
    self._stash = {}

  def stash(self, field_name):
    if self.instance.pk:
      attr = getattr(self.instance, field_name)
      self._stash[field_name] = attr.all()

  def apply(self, field_name, extra_values=[]):
    old = set(self._stash.pop(field_name, []))
    new = set(self.cleaned_data[field_name])
    new = new.union(set(extra_values))

    field = self._meta.model._meta.get_field_by_name(field_name)[0]
    objects = field.rel.through.objects

    # Create links to just-added objects.
    for new_object in (new-old):
      objects.get_or_create(**{
        field.m2m_field_name(): self.instance,
        field.m2m_reverse_field_name(): new_object
      })

    # Destroy links to just-removed objects.
    objects.filter(**{
      "%s__in" % field.m2m_reverse_field_name(): (old-new)
    }).delete()

  def save(self, creator=None):
    with transaction.commit_on_success():
      self.stash("user_profiles")
      self.stash("evidences")

      hunch = super(HunchForm, self).save(commit=False)
      if creator is not None:
        hunch.creator = creator

      hunch.save()

      hunch.tags = self.cleaned_data['tags']

      add_groups = self.cleaned_data['add_groups']
      group_members = []

      for group in add_groups:
        group_members.extend(group.members.all())

      self.apply("user_profiles", group_members)
      self.apply("evidences")

    return hunch
