#!/usr/bin/env python

from django import forms
from djtokeninput.fields import TokenField
from hunchworks import models


class InviteForm(forms.Form):
  hunch = forms.ModelChoiceField(models.Hunch.objects.all(), widget=forms.HiddenInput)

  recipients = TokenField(models.InviteProxy)

  message = forms.CharField(label="Personal message", widget=forms.Textarea, required=False,
    help_text="This message will be sent to every user which you invite, " +
              "along with a link to your hunch.")

  def send_invites(self, inviter):
    hunch = self.cleaned_data["hunch"]
    for invite_proxy in self.cleaned_data["recipients"]:
      hunch.invite(invite_proxy, inviter, self.cleaned_data["message"])
