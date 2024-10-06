from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.functional import cached_property

from apps.common.models import BaseModel
from apps.core.models import StudentProfile, Level, Department
from apps.portal.choices import SEMESTER_CHOICES, GRADE_CHOICES, REMARK_CHOICES


# Create your models here.


class Session(BaseModel):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Semester(BaseModel):
    session = models.ForeignKey(
        Session, null=True, on_delete=models.DO_NOTHING, related_name="semesters"
    )
    name = models.CharField(max_length=9, choices=SEMESTER_CHOICES, null=True)

    class Meta:
        get_latest_by = "created"

    def __str__(self):
        return f"{self.session.name} - {self.name}"


class GradeLevel(BaseModel):
    name = models.CharField(max_length=100)
    min_point = models.FloatField()
    max_point = models.FloatField()

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.name


class CourseGrade(BaseModel):
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    exam_score = models.IntegerField(null=True)
    point = models.IntegerField(null=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.grade


class Course(BaseModel):
    department = models.ForeignKey(
        Department, on_delete=models.DO_NOTHING, related_name="courses"
    )
    name = models.CharField(max_length=200, unique=True)
    semester = models.ForeignKey(
        Semester,
        on_delete=models.DO_NOTHING,
        related_name="courses",
        null=False,
        blank=False,
    )
    course_level = models.ForeignKey(
        Level, on_delete=models.DO_NOTHING, related_name="courses"
    )
    course_code = models.CharField(max_length=10, unique=True, null=False, blank=False)
    description = models.CharField(max_length=255, blank=True, null=False)
    unit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.department.name} - {self.name} ({self.course_level})"

    def course_registered_by_student(self, student):
        return self.registrations.filter(
            student=student, registered_status=True
        ).exists()


class CourseRegistration(BaseModel):
    semester = models.ForeignKey(
        Semester,
        on_delete=models.DO_NOTHING,
        related_name="course_registrations",
        null=True,
    )
    student = models.ForeignKey(
        StudentProfile, on_delete=models.DO_NOTHING, related_name="registrations"
    )
    course = models.ForeignKey(
        Course, related_name="registrations", on_delete=models.DO_NOTHING
    )
    exam_score = models.IntegerField(
        null=True, blank=True, default=0, validators=[MaxValueValidator(100)]
    )
    course_grade = models.ForeignKey(
        CourseGrade,
        on_delete=models.DO_NOTHING,
        related_name="course_registrations",
        null=True,
        blank=True,
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.DO_NOTHING,
        related_name="course_registrations",
        null=True,
    )
    registered_status = models.BooleanField(default=False)
    remark = models.CharField(
        max_length=6, null=True, blank=True, choices=REMARK_CHOICES
    )

    @cached_property
    def calculated_course_point_after_exam(self):
        return (
            self.course_grade.point * self.course.unit
            if self.course_grade
            else "Not calculated yet"
        )

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.student.get_department_name()} {self.course.name}"


class Result(BaseModel):
    registration = models.OneToOneField(
        CourseRegistration, on_delete=models.DO_NOTHING, related_name="result"
    )
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)

    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.registration.student.get_full_name()} {self.registration.course.name} - {self.grade}"
