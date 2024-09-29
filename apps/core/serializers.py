from django.contrib.auth import get_user_model, authenticate
from django.core import validators
from django.core.validators import validate_email
from rest_framework import serializers as sr, status

from apps.common.errors import ErrorCode
from apps.common.exceptions import RequestError

User = get_user_model()


def validate_email_address(value: str) -> str:
    """
    Validates an email address.
    Parameters:
        value (str): The email address to be validated.
    Returns:
        str: The validated email address
    """

    try:
        validate_email(value)
    except sr.ValidationError:
        raise sr.ValidationError("Invalid email address.")
    return value


class LoginSerializer(sr.Serializer):
    matric_no = sr.CharField(default="202409000001", max_length=12)
    password = sr.CharField(write_only=True, default="Validpass#1234")

    def validate(self, attrs):
        matric_no = attrs.get("matric_no")
        password = attrs.get("password")

        user = authenticate(matric_no=matric_no, password=password)

        if not user:
            raise RequestError(
                err_code=ErrorCode.INVALID_CREDENTIALS,
                err_msg="Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return {"user": user}


class RegisterSerializer(sr.Serializer):
    email = sr.CharField()
    password = sr.CharField(
        max_length=20,
        write_only=True,
        min_length=8,
        validators=[
            validators.RegexValidator(
                regex=r'[!@#$%^&*(),.?":{}|<>]',
                message="Password must contain at least one special character.",
            )
        ],
        default="Validpass#1234",
    )


class UserSerializer(sr.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")


class StudentProfileSerializer(sr.Serializer):
    user_info = UserSerializer(source="user")
    profile_id = sr.UUIDField(source="id")
    department = sr.CharField()
    level = sr.CharField()
    matric_no = sr.CharField()
    date_of_birth = sr.DateField()
    address = sr.CharField()
    phone_number = sr.CharField()
