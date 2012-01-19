#!/usr/bin/env python

import os
from django.conf import settings


def handle_uploaded_file(uploaded_file, dirname):
  dest_file = os.path.join(settings.MEDIA_ROOT, dirname, str(uploaded_file))
  dest_dir = os.path.dirname(dest_file)

  if not os.path.exists(dest_path):
    os.makedirs(dest_path)

  with open(dest_file, "wb+") as f:
    for chunk in uploaded_file.chunks():
      f.write(chunk)
