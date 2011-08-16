#!/usr/bin/python2.7
# Base views files for the HunchWorks application.
# Author: Auto created by DJANGO
# Date: 2011-06-1
# License:  This  program  is  free  software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the  Free Software Foundation; either version 3 of the License, or (at your
# option)  any later version. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.

import models

from django import http
from django.utils import simplejson

def skills(request):
  skills = models.HwSkill.objects.all()
  skills = skills.values_list('skill_id', 'skill_name')
  skills =  [{ "id": x[0], "name": x[1]} for x in skills]
  
  return http.HttpResponse( simplejson.dumps(skills) )


def tags(request):
  tags = models.HwTag.objects.all()
  tags = tags.values_list('tag_id', 'tag_name')
  tags =  [{ "id": x[0], "name": x[1]} for x in tags]

  return http.HttpResponse( simplejson.dumps(tags) )


