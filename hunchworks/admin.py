#!/usr/bin/env python

from hunchworks.models import *
from django.contrib import admin

admin.site.register(Album)
admin.site.register(Attachment)
admin.site.register(Course)
admin.site.register(Hunch)
admin.site.register(Evidence)
admin.site.register(Group)
admin.site.register(GroupConnection)
admin.site.register(Invitation)
admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(Skill)
admin.site.register(UserRole)
admin.site.register(Tag)


# Unregister the Django auth user, and re-register it with our
# related UserProfile inline.
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class UserProfileInline(admin.StackedInline):
  model = UserProfile

class UserProfileAdmin(UserAdmin):
  inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)