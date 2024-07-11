from django.contrib import admin

from apps.portal.models import *

# Register your models here.


admin.site.register([Course, Session, Semester, CourseRegistration, Result])
