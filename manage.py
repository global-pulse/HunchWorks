#!/usr/bin/python2.7
# Managing file for hunchWorks project.
# Author: Auto created by DJANGO
# Date: 2011-6-1
# License:  This  program  is  free  software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the  Free Software Foundation; either version 3 of the License, or (at your
# option)  any later version. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.


from django.core.management import execute_manager
import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write(
        'Error: Can\'t find the file "settings.y" in the directory containing '
        '%r. It appears you\'ve customized things.\nYou\'ll have to run '
        'django-admin.py, passing it your settings module.\n'
        % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    execute_manager(settings)
