from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'id',
        'username',
        'first_name',
        'last_name',
        'ban',
        'telegram_id',
        'telegram_chat_id',
        'remind_hours',
        'remind_enabled',
        'groups_fmt',
    ]

    fieldsets = [
        ['Authorization', {
            'fields': [
                'username',
                'telegram_id',
                'telegram_chat_id',
                'is_superuser',
                'is_staff',
                'ban',
                'groups'
            ]
        }
         ],
        ['Personal info', {
            'fields': [
                'first_name',
                'last_name',
                'remind_hours',
                'remind_enabled',
            ]
        }
         ],
    ]

    search_fields = ['username']
    ordering = ['id']
    readonly_fields = ['id']

    @admin.display(description='Groups', ordering='groups')
    def groups_fmt(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
