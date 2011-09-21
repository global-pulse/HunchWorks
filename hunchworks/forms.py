#!/usr/bin/env python

import json
from hunchworks import models, custom_fields
from django import forms
from django.db import transaction
from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from django.utils.datastructures import MultiValueDict, MergeDict


class TokenWidget(forms.TextInput):
  search_url = ""
  class_name = "error"

  def render(self, name, value, attrs=None):
    flat_value = ",".join(map(unicode, value or []))

    attrs["data-search-url"] = self.search_url
    attrs["class"] = self.class_name

    if value is not None:
      attrs["data-prepopulate"] = json.dumps([
        {"id": pk, "name": unicode(self.choices.queryset.get(pk=pk))}
        for pk in value
      ])

    return super(TokenWidget, self).render(
      name, flat_value, attrs)

  def value_from_datadict(self, data, files, name):
    values = data.get(name, "").split(",")
    return self.clean_keys(values)

  def clean_keys(self, values):
    return [int(x) for x in values if x.strip().isdigit()]

  def set_search_url(self, url):
    self.search_url = url
    
  def set_class_name(self, name):
    self.class_name = name


class TokenField(forms.ModelMultipleChoiceField):
  widget = TokenWidget
  query_set = models.Hunch.objects.all()
  
  def set_search_url(self, url):
    self.widget.set_search_url(url)
    
  def set_class_name(self, name):
    self.widget.set_class_name(name)
    
  def set_query_set(self, set):
    self.query_set = set

  def __init__(self, *args, **kwargs):
    super(TokenField, self).__init__(
      self.query_set,
      *args, **kwargs)


class HunchForm(ModelForm):
  tags = TokenField(required=False)
  tags.set_search_url("/tags")
  tags.set_class_name("tags")
  tags.set_query_set(models.Tag.objects.all())
  skills = TokenField(required=False)
  skills.set_search_url("/skills")
  skills.set_class_name("skills")
  skills.set_query_set(models.Skill.objects.all())
  languages = TokenField(required=False)
  languages.set_search_url("/languages")
  languages.set_class_name("languages")
  languages.set_query_set(models.Language.objects.all())
  user_profiles = TokenField(required=False)
  user_profiles.set_search_url("user/4/collaborators")
  user_profiles.set_class_name("userProfiles")
  user_profiles.set_query_set(models.UserProfile.objects.all())

  class Meta:
    model = models.Hunch
    exclude = (
      "creator", "time_created", "time_modified", "status",
    )
    
  def save(self, creator=None):
    with transaction.commit_on_success():
      old_up = set(self.instance.user_profiles.all() if self.instance.pk else [])
      new_up = set(self.cleaned_data["user_profiles"])

      hunch = super(HunchForm, self).save(commit=False)
      if creator is not None:
        hunch.creator = creator

      hunch.save()
      
      hunch.tags = self.cleaned_data['tags']
      hunch.languages = self.cleaned_data['languages']
      hunch.skills = self.cleaned_data['skills']
      

      for user_profile in (new_up-old_up):
        models.HunchUser.objects.get_or_create(
          user_profile=user_profile,
          hunch=hunch)

      models.HunchUser.objects.filter(
        user_profile__in=(old_up-new_up)).delete()

    return hunch


class EvidenceForm(ModelForm):
  class Meta:
    model = models.Evidence
    exclude = (
    'hunch_id', 'creator_id', 'evidence_strength', 'time_created',
    'time_modified', 'attachments', 'albums', 'hunch', 'evidence_tags'
    )


class GroupForm(ModelForm):
  members = TokenField(required=False,
    help_text="The HunchWorks members you wish to invite to this group.<br>" +
              "You can only invite members who you are connected with.")
  members.set_search_url("user/4/collaborators")
  members.set_class_name("members")
  members.set_query_set(models.UserProfile.objects.all())

  class Meta:
    model = models.Group
    exclude = ("logo")
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


class HomepageForm(ModelForm):
  class Meta:
    model = models.User

class UserForm(ModelForm):
  class Meta:
    model= models.UserProfile
    exclude = ("user")

class InvitePeople(forms.Form):
  invited_emails = custom_fields.MultiEmailField(widget=forms.Textarea(
    attrs={'cols': 30, 'rows': 10}))
  
  def save(self, user_id, hunch=None, *args, **kwargs):
    user = models.UserProfile.objects.get(pk=user_id)
    #hunch = models.Hunch.objects.get(pk=hunch_id)
    print self.cleaned_data
    #TODO( Chris: 8-15-2011): figure out how ot introspect invited_emails object instead
    # of using email_input
    for email_input in self.cleaned_data['invited_emails']:
      invitation = models.Invitation(
      invited_by = user,
      email = email_input,
      #hunch = hunch,
      )
      invitation.save()
    
