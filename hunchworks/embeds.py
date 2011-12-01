#!/usr/bin/env python

import json
import urlparse
from hunchworks.utils.data.worldbank import indicator as wb_indicator
from hunchworks.utils.data.worldbank import chart as wb_chart
from django.template.loader import render_to_string


def worldbank(url):
  if url.startswith("http://127.0.0.1:8000/explore?"):
    qs = urlparse.parse_qs(urlparse.urlparse(url).query)
    data = wb_indicator(qs["indicator"][0], qs["country"][0].split(","))
    countries, data = wb_chart(data)
    
    return render_to_string(
      "embeds/worldbank.html", {
        "flat_data": json.dumps(data),
        "flat_countries": json.dumps(countries)        
      }
    )
