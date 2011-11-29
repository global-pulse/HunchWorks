#!/usr/bin/env python

from hunchworks.events import utils


# post_save(sender=Hunch)
def hunch_created(sender, instance, created, **kwargs):
  hunch = instance
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


# post_save(sender=Comment)
def comment_posted(sender, instance, created, **kwargs):
  comment = instance
  if created:

    if comment.hunch_evidence:

      notify_users = set(comment.hunch_evidence.hunch.user_profiles.all())
      notify_users.add(comment.hunch_evidence.hunch.creator)

      for user_profile in notify_users:
        user_profile.create_event(
          "comment_posted_to_hunchevidence",
          comment=comment)


# user_invited(sender=Hunch)
def user_invited_to_hunch(sender, instance, inviter, invitee, message, **kwargs):
  invitee.create_event(
    "user_invited_to_hunch",
    hunch=instance,
    inviter=inviter,
    invitee=invitee,
    message=message)
