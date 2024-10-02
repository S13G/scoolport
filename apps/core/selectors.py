from django.contrib.auth import get_user_model

from .models import StudentProfile

User = get_user_model()


def authenticate(matric_no=None, password=None):
    try:
        profile = StudentProfile.objects.get(matric_no=matric_no)
        user = profile.user

        if user and user.check_password(password):
            return user
    except StudentProfile.DoesNotExist:
        return None
