#!/usr/bin/env python

from urlparse import parse_qs
from linkedin import linkedin
from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def linkedin_api_from_user_profile(user_profile):
  """
  """

  try:
    user_social_auth = user_profile.user.social_auth.get(provider="linkedin")
    data = parse_qs(user_social_auth.extra_data["access_token"])

  except ObjectDoesNotExist:
    return None

  # Hack: We want to use the proper Python LinkedIn API to perform queries,
  # but we've already authorized with the django_social. So extract the keys
  # from the UserSocialAuth model.

  api = linkedin.LinkedIn(settings.LINKEDIN_CONSUMER_KEY, settings.LINKEDIN_CONSUMER_SECRET, None)
  api._access_token_secret = str(data["oauth_token_secret"][0])
  api._access_token = str(data["oauth_token"][0])

  return api
