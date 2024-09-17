from django.db import models

from apps.common.models import BaseModel
from apps.core.models import StudentProfile, Level, Department
from apps.portal.choices import SEMESTER_CHOICES, GRADE_CHOICES


# Create your models here.

class Session(BaseModel):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Semester(BaseModel):
    session = models.ForeignKey(Session, null=True, on_delete=models.DO_NOTHING, related_name="semesters")
    name = models.CharField(max_length=9, choices=SEMESTER_CHOICES, null=True)

    def __str__(self):
        return f"{self.session.name} - {self.name}"


class Course(BaseModel):
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name="courses")
    name = models.CharField(max_length=200, unique=True)
    semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING, related_name="registrations", null=False,
                                 blank=False)
    course_level = models.ForeignKey(Level, on_delete=models.DO_NOTHING, related_name="courses")
    course_code = models.CharField(max_length=10, unique=True, null=False, blank=False)
    description = models.CharField(max_length=255, blank=True, null=False)
    unit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.department.name} - {self.name} ({self.course_level})"

    def course_registered_by_student(self, student):
        return self.registrations.filter(student=student, registered_status=True).exists()


class CourseRegistration(BaseModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.DO_NOTHING, related_name="registrations")
    course = models.ForeignKey(Course, related_name="registrations", on_delete=models.DO_NOTHING)
    registered_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.student.get_department_name()} {self.course.name}"


class Result(BaseModel):
    registration = models.OneToOneField(CourseRegistration, on_delete=models.DO_NOTHING, related_name="result")
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.registration.student.get_full_name()} {self.registration.course.name} - {self.grade}"
