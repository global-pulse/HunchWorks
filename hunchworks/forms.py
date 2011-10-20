#!/usr/bin/env python

import re
import json
from hunchworks import models, custom_fields, json_views
from django import forms
from django.db import transaction
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.safestring import mark_safe


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


class EvidenceWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    flat_widget = super(EvidenceWidget, self).render(
      name, value, attrs)

    try:
      evidence = self.choices.queryset.get(pk=value)
      previews = [self.render_one(evidence)]

    except:
      previews = []

    return render_to_string("evidences/widget.html", {
      "flat_widget": flat_widget,
      "help_text": self._help(),
      "previews": previews,
      "variety": "one"
    })

  def render_one(self, evidence):
    return render_to_string(
      "evidences/short.html",
      { "evidence": evidence })

  def _help(self):
    return "If JavaScript is disabled, enter an evidence ID."


class MultipleEvidenceWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    flat_widget = super(MultipleEvidenceWidget, self).render(
      name, self._flat_value(value), attrs)

    previews = map(
      self.render_one,
      self._value_objects(value))

    return render_to_string("evidences/widget.html", {
      "flat_widget": flat_widget,
      "help_text": self._help(),
      "previews": previews,
      "variety": "many"
    })

  def value_from_datadict(self, data, files, name):
    keys = map(unicode.strip, data.get(name, "").split(","))
    return [int(key) for key in keys if key.isdigit()]

  def render_one(self, evidence):
    return render_to_string(
      "evidences/short.html",
      { "evidence": evidence })

  def _help(self):
    return "If JavaScript is disabled, enter evidence IDs separated by commas."

  def _value(self, value):
    return value or []

  def _flat_value(self, value):
    return ", ".join(map(unicode, self._value(value)))

  def _value_objects(self, value):
    return self.choices.queryset.filter(
      pk__in=self._value(value))


class EvidenceField(forms.ModelChoiceField):
  widget = EvidenceWidget

  @classmethod
  def query_set(cls):
    return models.Evidence.objects.all()

  def __init__(self, *args, **kwargs):
    super(EvidenceField, self).__init__(
      self.query_set(), *args, **kwargs)


class EvidencesField(forms.ModelMultipleChoiceField):
  widget = MultipleEvidenceWidget

  @classmethod
  def query_set(cls):
    return models.Evidence.objects.all()

  def __init__(self, *args, **kwargs):
    super(EvidencesField, self).__init__(
      self.query_set(), *args, **kwargs)


class HunchForm(ModelForm):
  tags = TokenField(models.Tag, json_views.tags, required=False)
  languages = TokenField(models.Language, json_views.languages, required=False)
  skills = TokenField(models.Skill, json_views.skills, required=False)
  user_profiles = TokenField(models.UserProfile, json_views.collaborators, required=False)
  add_groups = TokenField(models.Group, json_views.user_groups, required=False)
  location = LocationField(required=False)
  evidences = EvidencesField(required=False)

  class Meta:
    model = models.Hunch
    exclude = (
      "creator", "time_created", "time_modified", "status"
    )

  def __init__(self, *args, **kwargs):
    self._stash = {}
    super(HunchForm, self).__init__(*args, **kwargs)

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
      hunch.languages = self.cleaned_data['languages']
      hunch.skills = self.cleaned_data['skills']
      
      add_groups = self.cleaned_data['add_groups']
      group_members = []

      for group in add_groups:
        group_members.extend(group.members.all())

      self.apply("user_profiles", group_members)
      self.apply("evidences")

    return hunch


class EmbedWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    widget = super(EmbedWidget, self).render(
      name, value, attrs)

    return mark_safe(u"""
      <div class="embed-widget">
        %s
      </div>
    """ % (widget))


class EmbedField(forms.CharField):
  widget = EmbedWidget


class AlbumForm(forms.ModelForm):
  evidences = EvidencesField(required=False)
  
  class Meta:
    model = models.Album


class EvidenceForm(ModelForm):
  tags = TokenField(models.Tag, json_views.tags, required=False)
  link = EmbedField(
    help_text='Enter an URL to be embedded. You can find a list of supported ' +
              'providers at <a href="http://embed.ly/providers">Embedly</a>.')

  class Meta:
    model = models.Evidence
    fields = (
      "title", "description", "link", "tags"
    )

  def save(self, creator=None):
    with transaction.commit_on_success():
      evidence = super(EvidenceForm, self).save(commit=False)

      if creator is not None:
        evidence.creator = creator

      evidence.save()
      return evidence




class GroupForm(ModelForm):
  members = TokenField(models.UserProfile, json_views.collaborators, required=False,
    help_text="The HunchWorks members you wish to invite to this group.<br>" +
              "You can only invite members who you are connected with.")

  class Meta:
    model = models.Group
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


class HunchCommentForm(ModelForm):
  class Meta:
    model = models.Comment
    fields = ("text",)


class CommentForm(forms.ModelForm):
  class Meta:
    model = models.Comment
    fields = ("text", "hunch_evidence")
    widgets = {
      "hunch_evidence": forms.HiddenInput()
    }

  def save(self, creator=None):
    comment = super(CommentForm, self).save(commit=False)

    if creator is not None:
      comment.creator = creator

    comment.save()
    return comment


class HomepageForm(ModelForm):
  class Meta:
    model = models.User


class UserForm(ModelForm):
  location_interests = TokenField(models.Location, json_views.locations, required=False)
  skills = TokenField(models.Skill, json_views.skills, required=False)
  languages = TokenField(models.Language, json_views.languages, required=False)
  class Meta:
    model= models.UserProfile
    exclude = ("user")


class InvitePeople(forms.Form):
  invited_emails = custom_fields.MultiEmailField(widget=forms.Textarea(
    attrs={'cols': 30, 'rows': 10}))

  def save(self, user_id, hunch=None, *args, **kwargs):
    user = models.UserProfile.objects.get(pk=user_id)
    #hunch = models.Hunch.objects.get(pk=hunch_id)

    #TODO( Chris: 8-15-2011): figure out how ot introspect invited_emails object instead
    # of using email_input
    for email_input in self.cleaned_data['invited_emails']:
      invitation = models.Invitation(
      invited_by = user,
      email = email_input,
      #hunch = hunch,
      )
      invitation.save()


class VoteChoiceRenderer(forms.widgets.RadioFieldRenderer):
  """
  Identical to Django's RadioFieldRenderer, with the addition of a "selected"
  class to the <li> containing the selected radio button, for easier styling.
  """

  def _ul(self):
    return '<ul>%s</ul>' % "".join(
      map(self._li, self))

  def _css_class(self, widget):
    label = widget.choice_label.lower().replace(" ", "-")
    css_class = re.sub("[^a-z\-]+", "", label)

    if(self.value == widget.choice_value):
      css_class += " selected"

    return css_class

  def _li(self, widget):
    return '<li class="%s">%s</li>' % (
      self._css_class(widget), unicode(widget))

  def render(self):
    return mark_safe('<div class="vote-widget">%s</div>' % (
      self._ul()))


class VoteForm(ModelForm):
  class Meta:
    model = models.Vote
    exclude = ("user_profile",)
    widgets = {
      "choice": forms.RadioSelect(renderer=VoteChoiceRenderer),
      "hunch_evidence": forms.HiddenInput()
    }

  def save(self, user_profile=None):
    with transaction.commit_on_success():
      vote_form = super(VoteForm, self).save(commit=False)
      hunch_evidence = self.cleaned_data["hunch_evidence"]
      
      if len(models.Vote.objects.filter(user_profile=user_profile, hunch_evidence=hunch_evidence)) > 0:
        vote = models.Vote.objects.get(
          user_profile=user_profile, 
          hunch_evidence=hunch_evidence)
        vote.choice = vote_form.choice
        vote.save()
      else:
        vote, created = models.Vote.objects.get_or_create(
          user_profile=user_profile, 
          hunch_evidence=hunch_evidence,
          choice=vote_form.choice)
        vote.save()

      return vote


class AddHunchEvidenceForm(forms.ModelForm):
  evidence = EvidenceField()
  vote     = forms.ChoiceField(choices=models.SUPPORT_CHOICES, widget=forms.RadioSelect(renderer=VoteChoiceRenderer))
  comment  = forms.CharField(widget=forms.Textarea, required=False,
    help_text="Tell other users how this evidence supports or refutes this " +
              "hunch.")

  class Meta:
    model = models.HunchEvidence
    fields = ("hunch", "evidence")
    widgets = {
      "hunch": forms.HiddenInput()
    }

  def save(self, user_profile=None):
    with transaction.commit_on_success():
      hunch_evidence = super(AddHunchEvidenceForm, self).save()

      if self.cleaned_data["comment"]:
        comment = models.Comment.objects.create(
          hunch_evidence=hunch_evidence,
          creator=user_profile,
          text=self.cleaned_data["comment"])

      vote = models.Vote.objects.create(
        hunch_evidence=hunch_evidence,
        user_profile=user_profile,
        choice=self.cleaned_data["vote"])

      return hunch_evidence
