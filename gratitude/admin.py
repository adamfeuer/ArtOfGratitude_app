from gratitude.gratitude.models import Setting, UserDetail, Gratitude
from django.contrib import admin

class SettingAdmin(admin.ModelAdmin):
    fields = ['name', 'value', 'description']

class UserDetailAdmin(admin.ModelAdmin):
   fields = ['user', 'no_messages']

class GratitudeAdmin(admin.ModelAdmin):
    fields = ['user_id', 'text' ]

admin.site.register(Setting, SettingAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(Gratitude, GratitudeAdmin)



