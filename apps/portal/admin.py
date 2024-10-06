from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from apps.portal.models import *


# Register your models here.


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("name", "semesters")
    list_per_page = 20
    search_fields = ("name",)

    @admin.display(ordering="semesters", description="Semesters")
    def semesters(self, session):
        url = (
            reverse("admin:portal_semester_changelist") + "?session=" + str(session.id)
        )

        return format_html(
            '<a href="{}">{} Semesters</a>', url, session.semesters_count
        )

    def get_queryset(self, request):
        return (
            super().get_queryset(request).annotate(semesters_count=Count("semesters"))
        )


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "name",
    )
    list_per_page = 20
    search_fields = (
        "session__name",
        "name",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "department",
        "semester",
        "course_level",
        "course_code",
        "unit",
    )
    list_per_page = 20
    search_fields = (
        "name",
        "department__name",
        "course_level__name",
    )

    @admin.display(ordering="department", description="Department")
    def department(self, obj):
        return obj.department.name

    @admin.display(ordering="Level", description="Course Level")
    def course_level(self, obj):
        return obj.course_level.name

    @admin.display(ordering="semester", description="Semester")
    def semester(self, obj):
        return obj.semester.name


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "student_level",
        "department",
        "course_name",
        "course_unit",
        "level",
        "registered_status",
        "course_grade",
        "exam_score",
        "course_point",
    )
    list_editable = (
        "registered_status",
        "exam_score",
        "course_grade",
    )
    list_per_page = 20
    search_fields = (
        "student__user__email",
        "course__name",
    )

    @admin.display(description="Student Level")
    def student_level(self, obj):
        return obj.student.level.name

    @admin.display(description="Course unit")
    def course_unit(self, obj):
        return obj.course.unit

    @admin.display(description="Course point after examination")
    def course_point(self, obj):
        return obj.calculated_course_point_after_exam

    @admin.display(description="Course grade")
    def course_grade(self, obj):
        return obj.course_grade.grade

    @admin.display(ordering="student__user__email", description="Student name")
    def student_name(self, obj):
        return obj.student.get_full_name()

    @admin.display(ordering="student__department", description="Department")
    def department(self, obj):
        return obj.student.get_department_name()

    @admin.display(ordering="Course name", description="Course Level")
    def course_name(self, obj):
        return obj.course.name

    # Override save_model to add custom validation
    def save_model(self, request, obj, form, change):
        # Check if the course is not registered and the user tries to add a grade or exam score
        if not obj.registered_status and (obj.exam_score or obj.course_grade):
            messages.error(
                request, "Cannot add a grade or score without registering the course."
            )
            return

        # Proceed with saving the object if validation passes
        super().save_model(request, obj, form, change)


@admin.register(CourseGrade)
class CourseGradeAdmin(admin.ModelAdmin):
    list_display = (
        "grade",
        "point",
        "exam_score",
    )
    list_editable = (
        "point",
        "exam_score",
    )
    list_per_page = 20
    search_fields = ("grade",)

    def has_add_permission(self, request):
        return False if self.model.objects.count() == 7 else True


@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "min_point",
        "max_point",
    )
    list_editable = (
        "min_point",
        "max_point",
    )
    list_per_page = 20
    search_fields = ("name",)

    def has_add_permission(self, request):
        return False if self.model.objects.count() == 6 else True


# @admin.register(Result)
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
