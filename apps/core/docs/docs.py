from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.serializers import LoginSerializer


def login_docs():
    return extend_schema(
        summary="Login Endpoint",
        description="""
        This endpoint allows a user to login with their matric number and password and this returns a refresh and access tokens 
        along with the student profile details.
        """,
        request=LoginSerializer,
        tags=["Authentication"],
        responses={
            200: OpenApiResponse(
                description="Success",
                response={"application/json"},
                examples=[
                    OpenApiExample(
                        name="Success",
                        value={
                            "status": "success",
                            "message": "Logged in successfully",
                            "data": {
                                "tokens": {"refresh": "<token>", "access": "<token>"},
                                "profile": {
                                    "user_info": {
                                        "id": "416e8c37-d9ad-4c73-9b51-d5d557d00e6e",
                                        "first_name": "John",
                                        "last_name": "Doe",
                                        "email": "student1@gmail.com",
                                    },
                                    "profile_id": "a27185ea-c6d6-4e81-ae5b-ff1ea1dc4967",
                                    "department": "Computer Science - Faculty of Computing and Informatics",
                                    "level": "100L",
                                    "matric_no": "202407000002",
                                    "date_of_birth": "2024-07-15",
                                    "address": "Lagos Island",
                                    "phone_number": "+234814170417",
                                },
                            },
                        },
                    )
                ],
            ),
        },
    )


def logout_docs():
    return extend_schema(
        summary="Logout",
        description="""
        This endpoint logs out an authenticated user by blacklisting their access token.
        The request should include the following data:

        - `refresh`: The refresh token used for authentication.
        """,
        tags=["Authentication"],
        responses={
            400: OpenApiResponse(
                response={"application/json"},
                description="Token is blacklisted",
                examples=[
                    OpenApiExample(
                        name="Blacklisted token response",
                        value={
                            "status": "failure",
                            "message": "Token is blacklisted",
                            "code": "invalid_entry",
                        },
                    )
                ],
            ),
            200: OpenApiResponse(
                response={"application/json"},
                description="Logged out successfully",
                examples=[
                    OpenApiExample(
                        name="Logout successful response",
                        value={
                            "status": "success",
                            "message": "Logged out successfully",
                        },
                    )
                ],
            ),
        },
    )


def refresh_docs():
    return extend_schema(
        summary="Refresh token",
        description="""
        This endpoint allows a user to refresh an expired access token.
        The request should include the following data:

        - `refresh`: The refresh token.
        """,
        tags=["Authentication"],
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Refreshed successfully",
                examples=[
                    OpenApiExample(
                        name="Refresh successful response",
                        value={
                            "status": "success",
                            "message": "Refreshed successfully",
                            "data": "access_token",
                        },
                    )
                ],
            ),
        },
    )
