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

  content_type = ContentType.objects.get_for_model(obj)

  bookmark_count = models.Bookmark.objects.filter(
    user_profile=context['request'].user.get_profile(),
    content_type=content_type,
    object_id=obj.id
  ).count()

  return {
    "object": obj,
    "content_type": content_type,
    "is_bookmarked": bookmark_count > 0
  }
