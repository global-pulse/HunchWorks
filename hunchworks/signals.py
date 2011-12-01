#!/usr/bin/env python

from django.dispatch import Signal

user_invited = Signal(providing_args=["instance", "inviter", "invitee", "message"])
