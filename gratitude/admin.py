from gratitude.gratitude.models import Setting, UserProfile, Message, UserDetail
from django.contrib import admin

class SettingAdmin(admin.ModelAdmin):
    fields = ['name', 'value', 'description']

class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user_id', 'days_left' ]

class MessageAdmin(admin.ModelAdmin):
   fields = ['user_id', 'email_address', 'message', 'send_at',
             'sent', 'sent_status', 'sent_error_message']

class UserDetailAdmin(admin.ModelAdmin):
   fields = ['user', 'no_messages']

admin.site.register(Setting, SettingAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserDetail, UserDetailAdmin)



