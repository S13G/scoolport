from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from .models import StudentProfile

User = get_user_model()


class MatricNoBackend(BaseBackend):
    def authenticate(self, request, matric_no=None, password=None):
        try:
            profile = StudentProfile.objects.get(matric_no=matric_no)
            user = profile.user
            if user.check_password(password):
                return user
        except StudentProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
