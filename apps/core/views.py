from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenBlacklistSerializer,
    TokenRefreshSerializer,
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
    TokenObtainPairView,
)

from apps.common.errors import ErrorCode
from apps.common.exceptions import RequestError
from apps.common.responses import CustomResponse
from apps.core.docs.docs import *
from apps.core.serializers import *

User = get_user_model()

# Create your views here.


"""
REGISTRATION
"""


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    throttle_classes = [UserRateThrottle]

    @login_docs()
    @transaction.atomic
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # authenticating user
        user = authenticate(request, email=email, password=password)

        if not user:
            raise RequestError(
                err_code=ErrorCode.INVALID_CREDENTIALS,
                err_msg="Invalid credentials",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # tokens
        tokens_response = super().post(request)
        tokens = {
            "refresh": tokens_response.data["refresh"],
            "access": tokens_response.data["access"],
        }

        # serialized_data
        profile = StudentProfileSerializer(user.profile).data
        response_data = {"tokens": tokens, "profile": profile}
        return CustomResponse.success(
            message="Logged in successfully", data=response_data
        )


class LogoutView(TokenBlacklistView):
    serializer_class = TokenBlacklistSerializer

    @logout_docs()
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return CustomResponse.success(message="Logged out successfully.")
        except TokenError:
            raise RequestError(
                err_code=ErrorCode.INVALID_ENTRY,
                err_msg="Token is blacklisted",
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class RefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    @refresh_docs()
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        except TokenError:
            raise RequestError(
                err_code=ErrorCode.INVALID_ENTRY,
                err_msg="Error refreshing token",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        access_token = serializer.validated_data["access"]
        return CustomResponse.success(
            message="Refreshed successfully", data=access_token
        )
