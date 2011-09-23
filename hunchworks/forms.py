#!/usr/bin/env python

import json
from hunchworks import models, custom_fields, json_views
from django import forms
from django.db import transaction
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from django.utils.datastructures import MultiValueDict, MergeDict


class TokenWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    flat_value = ",".join(map(unicode, value or []))

    if hasattr(self, "search_view"):
      attrs["data-search-url"] = reverse(self.search_view)

    attrs["class"] = self._class_name(
      attrs.get("class"), "token-input")

    if value is not None:
      attrs["data-prepopulate"] = json.dumps([
        {"id": pk, "name": unicode(self.choices.queryset.get(pk=pk))}
        for pk in value
      ])

    return super(TokenWidget, self).render(
      name, flat_value, attrs)

  @staticmethod
  def _class_name(class_name=None, extra=None):
    return " ".join(filter(None, [class_name, extra]))

  def value_from_datadict(self, data, files, name):
    values = data.get(name, "").split(",")
    return self.clean_keys(values)

  def clean_keys(self, values):
    return [int(x) for x in values if x.strip().isdigit()]


class TokenField(forms.ModelMultipleChoiceField):
  widget = TokenWidget

  @staticmethod
  def _class_name(value):
    return value.replace(" ", "-")

  def __init__(self, model, search_view, *args, **kwargs):
    super(TokenField, self).__init__(model.objects.all(), *args, **kwargs)
    self.widget.class_name = self._class_name(model._meta.verbose_name_plural)
    self.widget.search_view = search_view


class LocationWidget(forms.MultiWidget):
  def __init__(self, attrs=None):
    widgets = (
      forms.TextInput(attrs={"class": "lat"}),
      forms.TextInput(attrs={"class": "lng"}),
      forms.TextInput(attrs={"class": "name"}))
    super(LocationWidget, self).__init__(widgets, attrs)

  def decompress(self, value):
    if isinstance(value, int):
      value = models.Location.objects.get(pk=value)

    if value is not None:
      return [value.latitude, value.longitude, value.name]

    return [None, None, None]

  def render(self, name, value, attrs=None):

    # take note of the name before calling super, so we can access it from
    # format_output without reimplementing the whole of MultiWidget.render.
    self._name = name

    return super(LocationWidget, self).render(
      name, value, attrs)

  def format_output(self, rendered_widgets):
    lat, lng, name = rendered_widgets
    lat_id = "id_%s_0" % self._name
    lng_id = "id_%s_1" % self._name

    return """
      <div class="loc-widget">
        <ul class="type">
          <li class="active" data-type="latlng">GIS Coordinates</li>
          <li data-type="map">Pin on Map</li>
          <li data-type="name">Location Name</li>
        </ul>
        <div class="latlng">
          <div class="widgets">
            %s
            %s
            <div class="clear-hack"></div>
          </div>
          <div class="labels">
            <label class="lat" for="%s">Latitude</label>
            <label class="lng" for="%s">Longitude</label>
            <div class="clear-hack"></div>
          </div>
        </div>
        <div class="map hidden"></div>
        <div class="name hidden">%s</div>
      </div>
    """ % (lat, lng, lat_id, lng_id, name)


class LocationField(forms.MultiValueField):
  widget = LocationWidget

  def __init__(self, *args, **kwargs):
    fields = (forms.DecimalField(), forms.DecimalField(), forms.CharField())
    super(LocationField, self).__init__(fields, *args, **kwargs)

  def compress(self, data_list):
    if data_list:
      return models.Location.objects.create(
        latitude  = data_list[0],
        longitude = data_list[1],
        name      = data_list[2])




class HunchForm(ModelForm):
  tags = TokenField(models.Tag, json_views.tags, required=False)
  skills = TokenField(models.Skill, json_views.skills, required=False)
  user_profiles = TokenField(models.UserProfile, json_views.collaborators, required=False)
  location = LocationField(required=False)

  class Meta:
    model = models.Hunch
    exclude = (
      "creator", "time_created", "time_modified", "status"
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
  members = TokenField(models.UserProfile, json_views.collaborators, required=False,
    help_text="The HunchWorks members you wish to invite to this group.<br>" +
              "You can only invite members who you are connected with.")

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
