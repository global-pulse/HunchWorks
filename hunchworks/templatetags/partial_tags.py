#!/usr/bin/env python

from django.template.loader import render_to_string
from django import template
register = template.Library()


@register.simple_tag(takes_context=True)
def partial(context, obj):

  template = "includes/%s/short.html" %\
    unicode(obj._meta.verbose_name_plural)

  context.update({
    obj._meta.verbose_name: obj,  # old and busted
    "object": obj                 # new hotness
  })

  return render_to_string(
    template, context
  )
