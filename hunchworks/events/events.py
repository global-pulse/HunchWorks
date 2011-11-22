#!/usr/bin/env python

from hunchworks.events import utils


# post_save(sender=Hunch)
def hunch_created(sender, instance, created, **kwargs):
  hunch = hunch
  if created:

    notify_users = set(hunch.user_profiles.all())
    notify_users.add(hunch.creator)

    for user_profile in notify_users:
      user_profile.create_event(
        "hunch_created",
        hunch=hunch)


# post_save(sender=HunchEvidence)
def evidence_attached(sender, instance, created, **kwargs):
  hunch_evidence = instance
  if created:

    notify_users = set(hunch_evidence.hunch.user_profiles.all())
    notify_users.add(hunch_evidence.evidence.creator)
    notify_users.add(hunch_evidence.hunch.creator)

    for user_profile in notify_users:
      user_profile.create_event(
        "evidence_attached",
        hunch_evidence=hunch_evidence)
