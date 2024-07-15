from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from apps.portal.models import *


# Register your models here.

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "semesters"
    )
    list_per_page = 20
    search_fields = ("name",)

    @admin.display(ordering="semesters", description="Semesters")
    def semesters(self, session):
        url = reverse("admin:portal_semester_changelist") + "?session=" + str(session.id)

        return format_html('<a href="{}">{} Semesters</a>', url, session.semesters_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(semesters_count=Count("semesters"))


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "name",
    )
    list_per_page = 20
    search_fields = ("session__name", "name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "department",
        "course_level",
        "course_code",
        "unit",
    )
    list_per_page = 20
    search_fields = ("name", "department__name", "course_level__name",)


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "semester",
        "department",
    )
    list_per_page = 20
    search_fields = ("student__user__email", "course__name",)

    @admin.display(ordering="student__department", description="Department")
    def department(self, obj):
        return obj.student.get_department_name()


admin.site.register(Result)
# class ResultAdmin(admin.ModelAdmin):
#     list_display = (
#         "student",
#         "course",
#         "score",
#     )
#     list_per_page = 20
#     search_fields = ("student__user__email", "course__name",)
#
#     @admin.display(ordering="student__department", description="Department")
#     def department(self, obj):
#         return obj.student.get_department_name()
