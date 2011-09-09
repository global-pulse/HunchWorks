#!/usr/bin/env python

from hunchworks.models import *
from django.contrib import admin

admin.site.register(UserProfile)
admin.site.register(Connection)
admin.site.register(Hunch)
admin.site.register(Evidence)
admin.site.register(Group)
admin.site.register(UserProfileGroup)
admin.site.register(Attachment)
admin.site.register(Album)
admin.site.register(Education)
admin.site.register(Course)
admin.site.register(Language)
admin.site.register(Location)
admin.site.register(Tag)
admin.site.register(Role)
admin.site.register(Skill)
admin.site.register(UserProfileSkill)
admin.site.register(HunchSkill)
admin.site.register(Invitation)


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