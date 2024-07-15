from django.contrib.auth import get_user_model
from django.core import validators
from django.core.validators import validate_email
from rest_framework import serializers as sr

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


class RegisterSerializer(sr.Serializer):
    email = sr.CharField()
    password = sr.CharField(max_length=20, write_only=True, min_length=8, validators=[validators.RegexValidator(
        regex=r'[!@#$%^&*(),.?":{}|<>]',
        message="Password must contain at least one special character."
    )], default="Validpass#1234")


class LoginSerializer(sr.Serializer):
    email = sr.CharField(validators=[validate_email_address], default="student1@gmail.com")
    password = sr.CharField(write_only=True, default="Validpass#1234")


class UserSerializer(sr.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class StudentProfileSerializer(sr.Serializer):
    user_info = UserSerializer(source="user")
    profile_id = sr.UUIDField(source="id")
    department = sr.CharField()
    level = sr.CharField()
    matric_no = sr.CharField()
    date_of_birth = sr.DateField()
    address = sr.CharField()
    phone_number = sr.CharField()
