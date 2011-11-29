#!/usr/bin/env python

from django import forms


class ExploreWorldBankForm(forms.Form):
  indicator = forms.CharField()
  country = forms.CharField()
