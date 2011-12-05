#!/usr/bin/env python

from hunchworks.events import utils


def _set(*objects):
  s = set()

  for obj in objects:
    try:
      s.update(obj)

    except TypeError:
      s.add(obj)

  return s


def _attach(event, targets):
  for obj in targets:
    utils.attach_event(event, obj)


# post_save(sender=Hunch)
def hunch_created(sender, instance, created, **kwargs):
  hunch = instance
  if created:

    event = utils.create_event(
      "hunch_created",
      hunch=hunch
    )

    targets = _set(
      hunch,
      hunch.creator,
      hunch.user_profiles.all()
    )

    _attach(event, targets)


# post_save(sender=HunchEvidence)
def evidence_attached(sender, instance, created, **kwargs):
  hunch_evidence = instance
  if created:

    event = utils.create_event(
      "evidence_attached",
      hunch_evidence=hunch_evidence
    )

    targets = _set(
      hunch_evidence.hunch,
      hunch_evidence.evidence,
      hunch_evidence.evidence.creator,
      hunch_evidence.hunch.creator,
      hunch_evidence.hunch.user_profiles.all()
    )

    _attach(event, targets)


# post_save(sender=Comment)
def comment_posted(sender, instance, created, **kwargs):
  comment = instance
  if created:

    if comment.hunch_evidence:

      event = utils.create_event(
        "comment_posted_to_hunchevidence",
        comment=comment
      )

      targets = _set(
        comment.hunch_evidence.hunch,
        comment.hunch_evidence.hunch.creator,
        comment.hunch_evidence.creator,
        comment.hunch_evidence.hunch.user_profiles.all()
      )

      _attach(event, targets)

    elif comment.hunch:

      event = utils.create_event(
        "comment_posted_to_hunch",
        comment=comment
      )

      targets = _set(
        comment.hunch,
        comment.hunch.creator,
        comment.hunch.user_profiles.all()
      )

      _attach(event, targets)



# user_invited(sender=Hunch)
def user_invited_to_hunch(sender, instance, inviter, invitee, message, **kwargs):
  hunch = instance

  event = utils.create_event(
    "user_invited_to_hunch",
    hunch=hunch,
    inviter=inviter,
    invitee=invitee,
    message=message
  )

  targets = _set(
    hunch,
    inviter,
    invitee
  )

  _attach(event, targets)
