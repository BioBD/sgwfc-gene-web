from django.contrib import admin
from logger.models import Log
from django.shortcuts import reverse
from django.utils.html import format_html


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    def link_to_user(self, obj):
        if obj.user is None:
            return '-'

        link = reverse("admin:project_usuario_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', link, obj.user.username)

    link_to_user.short_description = 'user'
    list_display = ('event', 'link_to_user', 'ip', 'description', 'time')
