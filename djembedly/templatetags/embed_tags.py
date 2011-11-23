#!/usr/bin/env python

from djembedly.utils import url_to_html

from django import template
register = template.Library()


@register.simple_tag
def embed(url):
  """
  Return an HTML fragment to embed the content found at ``url``.
  """

  return url_to_html(url)
