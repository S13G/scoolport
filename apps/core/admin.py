from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as DjangoGroup

from apps.core.forms import CustomUserCreationForm, CustomUserChangeForm
from apps.core.models import *


class Group(DjangoGroup):
    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"
        proxy = True


class GroupAdmin(BaseGroupAdmin):
    pass


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = (
        "first_name",
        "last_name",
        "email",
        "is_staff",

    )
    list_display_links = (
        "email",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_per_page = 20
    fieldsets = (
        (
            "Login Credentials",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "raw_password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "groups",
                    "user_permissions"
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            "Personal Information",
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "raw_password",
                    "is_staff",
                ),
            },
        ),
    )
    readonly_fields = ("created", "updated",)
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "department",
        "level",
        "matric_no",
    )
    list_per_page = 20
    search_fields = (
        "matric_no",
        "user__email",
        "user__first_name",
        "user__last_name",
        "level__name",
    )


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.unregister(DjangoGroup)
admin.site.register([Level, Department, Faculty])
