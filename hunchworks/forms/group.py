#!/usr/bin/env python

from django import forms
from django.db import transaction
from djtokeninput.fields import TokenField
from hunchworks.fields import LocationField
from hunchworks import models


class GroupForm(forms.ModelForm):
  members = TokenField(models.UserProfile, required=False,
    help_text="The HunchWorks members you wish to invite to this group.<br>" +
              "You can only invite members who you are connected with.")

  location = LocationField(required=False,
    help_text="If the evidence is relative to a specific location, you can mark it here.")

  class Meta:
    model = models.Group
    exclude = ("type", "privacy")
    widgets = {
      'name': forms.TextInput(attrs={ 'size': 50 }),
      'abbreviation': forms.TextInput(attrs={ 'size': 15 })
    }

  def save(self):
    with transaction.commit_on_success():
      old_m = set(self.instance.members.all() if self.instance.pk else [])
      new_m = set(self.cleaned_data["members"])

      # Save the Group without saving the many-to-many members field. This is a
      # hack, but is preferable to reimplementing the ModelForm.save method.
      group = super(GroupForm, self).save(commit=False)
      group.save()

      for user_profile in (new_m-old_m):
        models.UserProfileGroup.objects.get_or_create(
          user_profile=user_profile,
          group=group)

      models.UserProfileGroup.objects.filter(
        user_profile__in=(old_m-new_m)).delete()

    return group
