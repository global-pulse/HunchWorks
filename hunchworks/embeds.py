#!/usr/bin/env python

import json
import urlparse
from hunchworks.utils.data.worldbank import chart as wb_chart
from django.template.loader import render_to_string


def worldbank(url):
  if url.startswith("http://localhost:8000/evidence/explore?"):
    qs = urlparse.parse_qs(urlparse.urlparse(url).query)
    data = wb_chart(qs["indicator"][0], qs["country"])

    return render_to_string(
      "embeds/worldbank.html", {
        "data": json.dumps(data)
      }
    )
