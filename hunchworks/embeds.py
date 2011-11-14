#!/usr/bin/env python

import re
import json
import urlparse
from embedly import Embedly
from hunchworks.utils.data.worldbank import chart as wb_chart
from django.template.loader import render_to_string
from django.conf import settings


def embedly(url):
  try:
    client = Embedly(settings.EMBEDLY_KEY)
    obj = client.oembed(url)

  except:
    return None

  if obj.type == "photo":
    return '<a href="%s" class="embed"><img src="%s"></a>' % (
      obj.url, obj.url)

  return obj


def worldbank(url):
  if url.startswith("http://localhost:8000/evidence/explore?"):
    qs = urlparse.parse_qs(urlparse.urlparse(url).query)
    data = wb_chart(qs["indicator"][0], qs["country"])

    return render_to_string(
      "embeds/worldbank.html", {
        "data": json.dumps(data)
      }
    )
