#!/usr/bin/env python

from django import forms
from django.utils.safestring import mark_safe
from hunchworks import models
from hunchworks.fields import VoteField


class VoteForm(forms.ModelForm):
  choice = VoteField()

  class Meta:
    model = models.Vote
    exclude = ("user_profile", "time_updated")
    widgets = {
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