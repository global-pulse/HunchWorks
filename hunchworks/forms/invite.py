#!/usr/bin/env python

from django import forms
from djtokeninput.fields import TokenField
from hunchworks import models


class InviteForm(forms.Form):
  recipients = TokenField(models.InviteProxy)

  message = forms.CharField(label="Personal message", widget=forms.Textarea, required=False,
    help_text="This message will be sent to every user which you invite, " +
              "along with a link to your hunch.")
