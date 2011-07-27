#!/usr/bin/python2.7
# Forms used in the project
# Author: Auto created by Texas
# Date: 2011-06-20
# License:  This  program  is  free  software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the  Free Software Foundation; either version 3 of the License, or (at your
# option)  any later version. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.

import models

from django.forms import ModelForm

class SignUpForm(ModelForm):
  class Meta:
    model = models.HwUser
    
class HomepageForm(ModelForm):
  class Meta:
    model = models.HwUser
