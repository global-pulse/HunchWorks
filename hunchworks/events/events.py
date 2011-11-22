#!/usr/bin/env python

from hunchworks.events import utils


def hunch_created(sender, instance, created, **kwargs):
  if created:

    notify_users = set(instance.user_profiles.all())
    notify_users.add(instance.creator)

    for user_profile in notify_users:
      user_profile.create_event(
        "hunch_created",
        hunch=instance)
