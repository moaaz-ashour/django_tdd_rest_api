from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# this hook is needed to make django projects translatable,
# Wrap the texts with this if you want django to automatically translate
from django.utils.translation import gettext as _

from core import models

# This class is used just for the admin interface.
# Nothing changes except the way admin page looks
class UserAdmin(BaseUserAdmin):
    ordering = ['id']

    # fields to be included in list users page
    list_display = ['email', 'name']

    # fields to be included on change user page (edit page)
    fieldsets = (
        (
            None, 
            {'fields': ('email', 'password')}
        ),
        (
            _('Personal Info'), 
            {'fields': ('name',)}
        ),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (
            _('Important dates'),
             {'fields': ('last_login',)}
        )
    )
    
admin.site.register(models.User, UserAdmin)