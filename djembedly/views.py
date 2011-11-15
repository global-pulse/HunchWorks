#!/usr/bin/env python

import json
from djembedly.utils import url_to_html
from django import http


def preview(req):
  url = req.GET.get("url", None)

  data = {
    "preview": url_to_html(url),
    "url": url
  }

  return http.HttpResponse(
    json.dumps(data),
    mimetype="application/json")
