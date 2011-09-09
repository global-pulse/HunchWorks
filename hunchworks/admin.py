import models
from django.contrib import admin

### EXAMPLE ###
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email')
#     search_fields = ('first_name', 'last_name')
 
# admin.site.register(Publisher)
# admin.site.register(Author, AuthorAdmin)


admin.site.register(models.UserProfile)
admin.site.register(models.Hunch)
admin.site.register(models.Tag)
admin.site.register(models.Skill)
admin.site.register(models.SkillConnections)
