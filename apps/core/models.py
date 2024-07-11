import string

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.crypto import get_random_string

from apps.common.models import BaseModel
from apps.core.managers import CustomUserManager
from utils.utils import generate_student_matric_no


# Create your models here.


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True, null=True)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.password:
            characters = string.ascii_letters + string.digits + string.punctuation
            self.password = get_random_string(length=12, allowed_chars=characters)
        super().save(*args, **kwargs)


class Level(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Faculty(BaseModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return self.name


class Department(BaseModel):
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING, related_name="departments")
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'faculty'], name='unique_department')
        ]


class StudentProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="profile")
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name="students")
    level = models.ForeignKey(Level, on_delete=models.DO_NOTHING, related_name="students")
    matric_no = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def get_full_name(self):
        return self.user.get_full_name()

    def get_department_name(self):
        return self.department.name

    def __str__(self):
        return f"{self.get_full_name()} ({self.matric_no})"

    def save(self, *args, **kwargs):
        if not self.matric_no:
            generate_student_matric_no(instance=self)
        super().save(*args, **kwargs)
