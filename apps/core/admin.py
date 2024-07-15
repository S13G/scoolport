from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

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
        "full_name",
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

    @admin.display(description="Full Name")
    def full_name(self, obj):
        return obj.get_full_name()


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "departments",
    )
    list_per_page = 20
    search_fields = (
        "name",
    )

    @admin.display(ordering="departments", description="Departments")
    def departments(self, faculty):
        url = reverse("admin:core_department_changelist") + "?faculty=" + str(faculty.id)

        return format_html('<a href="{}">{} Departments</a>', url, faculty.departments_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(departments_count=Count("departments"))


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "faculty",
        "students",
    )
    list_per_page = 20
    search_fields = ("name",)

    @admin.display(ordering="students", description="Students")
    def students(self, department):
        url = reverse("admin:core_studentprofile_changelist") + "?department=" + str(department.id)

        return format_html('<a href="{}">{} Students</a>', url, department.students_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(students_count=Count("students"))


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
    list_per_page = 20

    def has_add_permission(self, request):
        return False if self.model.objects.count() == 5 else True


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.unregister(DjangoGroup)
