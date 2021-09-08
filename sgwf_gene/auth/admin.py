from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from sgwf_gene.mailer import send_email


class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        if 'is_active' in form.changed_data and obj.is_active:
            # active state was changed and the user is now active,
            # send email telling the user their account was activated
            send_email(obj.email, 1, {
                'user': obj
            })

        super().save_model(request, obj, form, change)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
