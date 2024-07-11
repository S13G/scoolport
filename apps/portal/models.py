from django.db import models

from apps.common.models import BaseModel
from apps.core.models import StudentProfile, Level, Department


# Create your models here.

class Semester(BaseModel):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Session(BaseModel):
    semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING, related_name="sessions")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.semester.name} - {self.name}"


class Course(BaseModel):
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name="courses")
    name = models.CharField(max_length=200, unique=True)
    course_level = models.ForeignKey(Level, on_delete=models.DO_NOTHING, related_name="courses")
    course_code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)
    unit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.department.name} - {self.name} ({self.course_level})"


class CourseRegistration(BaseModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.DO_NOTHING, related_name="registrations")
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name="registrations")
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, related_name="registrations")

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.student.get_department_name()} {self.course} ({self.session})"


class Result(BaseModel):
    registration = models.OneToOneField(CourseRegistration, on_delete=models.DO_NOTHING, related_name="result")
    grade = models.CharField(max_length=2)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.registration.student.get_full_name()} {self.registration.course.name} - {self.grade}"
