#!/usr/bin/env python

import math
from django import template
from django.contrib.contenttypes.models import ContentType
from hunchworks import models
register = template.Library()


@register.inclusion_tag("templatetags/bookmark.html", takes_context=True)
def bookmarks(context, obj):

  # Silently abort if the request isn't available.
  if "request" not in context:
    return { }

  # Silently abort if the user isn't logged in, since anonymous users can't
  # bookmark things. (They shouldn't even be *seeing* bookmarkable objects
  # right now, but that will probably change.)
  user = context["request"].user
  if not user.is_authenticated():
    return { }

  content_type = ContentType.objects.get_for_model(obj)

  bookmark_count = models.Bookmark.objects.filter(
    user_profile=user.get_profile(),
    content_type=content_type,
    object_id=obj.id
  ).count()

  return {
    "object": obj,
    "content_type": content_type,
    "is_bookmarked": bookmark_count > 0
  }
