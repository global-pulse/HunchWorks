#!/usr/bin/env python

import math
from django import template
from django.contrib.contenttypes.models import ContentType
from hunchworks import models
register = template.Library()


@register.inclusion_tag("templatetags/bookmark.html", takes_context=True)
def bookmarks(context, object):
  object_type = ContentType.objects.get_for_model(object)
  bookmarked = False
  try:
    bookmark = models.Bookmark.objects.get(content_type=object_type.id, object_id=object.id, user_profile=context['request'].user.get_profile())
    bookmarked = True
  except models.Bookmark.DoesNotExist:
    bookmarked = False
  return {"object":object, "bookmarked":bookmarked, "object_type": object_type}