#!/usr/bin/env python

import os
from django.conf import settings


def handle_uploaded_file(f, dest):
  dest_path = settings.MEDIA_ROOT + dest
  #dest_path = settings.MEDIA_ROOT + '/profile_images/'
  if not os.path.exists(dest_path):
    os.makedirs(dest_path)
  destination = open(dest_path + str(f) , 'wb+')
  for chunk in f.chunks():
      destination.write(chunk)
  destination.close()