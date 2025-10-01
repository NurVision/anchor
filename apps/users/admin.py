from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "email", "username", "display_name", "is_active", "is_staff")
    list_display_links = ("id", "email", "username",)
    search_fields = ("email", "username", "display_name")
    list_filter = ("is_active", "is_staff")

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal_info'), {'fields': ('username', 'display_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'display_name', 'password1', 'password2', 'is_staff',
                       'is_active'),
        }),
    )

    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)