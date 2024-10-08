from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
)

from apps.portal.serializers import RegisterCourseSerializer, UnregisterCourseSerializer


def retrieve_session_docs():
    return extend_schema(
        summary="Retrieve all sessions",
        description="""
        This endpoint allows an authenticated user to retrieve all sessions for course registration
        """,
        tags=["Portal"],
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Retrieved successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Retrieved successfully",
                            "data": [
                                {
                                    "id": "932af8bb-3e26-4d41-88da-368bce130834",
                                    "name": "2023/2024 Academic Session",
                                }
                            ],
                        },
                    )
                ],
            ),
        },
    )


def retrieve_semester_docs():
    return extend_schema(
        summary="Retrieve all semesters",
        description="""
        This endpoint allows an authenticated user to retrieve all semesters pertaining to a specific session
        for course registration
        """,
        tags=["Portal"],
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Retrieved successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Retrieved successfully",
                            "data": [
                                {
                                    "id": "acd93042-9441-4329-bb64-ecae0ff357f5",
                                    "name": "Harmattan",
                                },
                                {
                                    "id": "d805a708-1797-4243-b122-be1ef5975e10",
                                    "name": "Rain",
                                },
                            ],
                        },
                    )
                ],
            ),
        },
    )


def retrieve_level_docs():
    return extend_schema(
        summary="Retrieve all levels",
        description="""
        This endpoint allows an authenticated user to retrieve all levels for course registration
        """,
        tags=["Portal"],
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Retrieved successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Retrieved successfully",
                            "data": [
                                {
                                    "id": "c05dce72-bb78-413d-8b8a-489e6daca85b",
                                    "name": "500L",
                                },
                                {
                                    "id": "ed3d84b2-59f9-4e89-9bfd-5d95dda31bb9",
                                    "name": "400L",
                                },
                                {
                                    "id": "c5964217-7eaa-4a49-b837-7904214deb3c",
                                    "name": "300L",
                                },
                                {
                                    "id": "accfa5cf-ee1e-4c1d-9601-23e41df92fe9",
                                    "name": "200L",
                                },
                                {
                                    "id": "d92202e4-93d7-4c4a-bbf6-ef11c0ea6507",
                                    "name": "100L",
                                },
                            ],
                        },
                    )
                ],
            ),
        },
    )


def retrieve_courses_to_register_docs():
    return extend_schema(
        summary="Retrieve courses",
        description="""
        This endpoint allows an authenticated user to retrieve courses he/she wants to register
        Optional Query Params to pass: semester, level. Pass in their ID, search (Course code)
        Example: ?semester=932af8bb-3e26-4d41-88da-368bce130834
        Example: ?level=c05dce72-bb78-413d-8b8a-489e6daca85b
        Example: ?semester=932af8bb-3e26-4d41-88da-368bce130834&level=c05dce72-bb78-413d-8b8a-489e6daca85b
        Example: ?search=CSC103
        """,
        tags=["Portal"],
        parameters=[
            OpenApiParameter("semester", OpenApiTypes.STR, description="Semester ID"),
            OpenApiParameter("level", OpenApiTypes.STR, description="Level ID"),
            OpenApiParameter(
                "search", OpenApiTypes.STR, description="Search course code"
            ),
        ],
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Retrieved successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Retrieved successfully",
                            "data": [
                                {
                                    "id": "d5f59de7-9a39-4c04-a910-cf36d89df89d",
                                    "name": "Computer Science 3",
                                    "course_code": "CSC103",
                                    "unit": 3,
                                    "is_registered": True,
                                },
                                {
                                    "id": "41a50119-02b3-47bd-acff-6392e7d823ab",
                                    "name": "Cloud Engineering 2",
                                    "course_code": "CLE105",
                                    "unit": 3,
                                    "is_registered": True,
                                },
                                {
                                    "id": "910048b1-e8ae-4092-89e2-29c7470a89ee",
                                    "name": "Cloud Engineering",
                                    "course_code": "CLE104",
                                    "unit": 3,
                                    "is_registered": True,
                                },
                                {
                                    "id": "ddebe7be-ddcf-43f3-9ec8-0c757306e6fa",
                                    "name": "Computer Science 2",
                                    "course_code": "CSC102",
                                    "unit": 2,
                                    "is_registered": False,
                                },
                                {
                                    "id": "b0fb72d5-d366-48ce-ba89-4716516a0417",
                                    "name": "Computer Science 1",
                                    "course_code": "CSC101",
                                    "unit": 5,
                                    "is_registered": False,
                                },
                            ],
                        },
                    )
                ],
            ),
        },
    )


def retrieve_registered_courses_docs():
    return extend_schema(
        summary="Retrieve registered courses",
        description="""
        This endpoint allows an authenticated user to retrieve registered courses
        """,
        tags=["Portal"],
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Retrieved successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Retrieved successfully",
                            "data": {
                                "courses": [
                                    {
                                        "id": "584e740d-5aff-4b2b-8d13-1e1fa69a9d80",
                                        "course__id": "d5f59de7-9a39-4c04-a910-cf36d89df89d",
                                        "course__name": "Computer Science 3",
                                        "course__unit": 3,
                                        "registered_status": True,
                                    },
                                    {
                                        "id": "c402a9df-4841-4095-a89e-bb3735eba2ec",
                                        "course__id": "910048b1-e8ae-4092-89e2-29c7470a89ee",
                                        "course__name": "Cloud Engineering",
                                        "course__unit": 3,
                                        "registered_status": True,
                                    },
                                    {
                                        "id": "52d13745-eeea-47c5-ada4-077802063877",
                                        "course__id": "41a50119-02b3-47bd-acff-6392e7d823ab",
                                        "course__name": "Cloud Engineering 2",
                                        "course__unit": 3,
                                        "registered_status": True,
                                    },
                                ],
                                "total_units": 9,
                            },
                        },
                    ),
                ],
            ),
        },
    )


def register_courses_docs():
    return extend_schema(
        summary="Register courses",
        description="""
        This endpoint allows an authenticated user to register courses
        """,
        tags=["Portal"],
        request=RegisterCourseSerializer,
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Registered successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Registered successfully",
                        },
                    ),
                ],
            ),
        },
    )


def unregister_course_docs():
    return extend_schema(
        summary="Unregister courses",
        description="""
        This endpoint allows an authenticated user to unregister courses
        """,
        tags=["Portal"],
        request=UnregisterCourseSerializer,
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Unregistered successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Unregistered successfully",
                        },
                    ),
                ],
            ),
        },
    )


def retrieve_all_semesters_registered_courses_docs():
    return extend_schema(
        summary="Retrieve all semesters registered courses",
        description="""
        This endpoint allows an authenticated user to retrieve all semesters registered courses
        """,
        tags=["Portal"],
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Retrieved successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Retrieved successfully",
                            "data": {
                                "2024/2025 Academic Session 100LRain": {
                                    "courses": [
                                        {
                                            "id": "b1dc9a0e-a16e-4ca1-9c00-6477b8178940",
                                            "course__id": "b0fb72d5-d366-48ce-ba89-4716516a0417",
                                            "course__name": "Computer Science 1",
                                            "course__unit": 5,
                                            "registered_status": True,
                                        },
                                        {
                                            "id": "916a0ee5-2220-4242-b726-334248e914b2",
                                            "course__id": "ddebe7be-ddcf-43f3-9ec8-0c757306e6fa",
                                            "course__name": "Computer Science 2",
                                            "course__unit": 2,
                                            "registered_status": True,
                                        },
                                        {
                                            "id": "26893255-eb2e-4eb8-8fff-c71af7c2fa6c",
                                            "course__id": "910048b1-e8ae-4092-89e2-29c7470a89ee",
                                            "course__name": "Cloud Engineering",
                                            "course__unit": 3,
                                            "registered_status": True,
                                        },
                                        {
                                            "id": "1519ef10-f7cf-4711-882a-98e72926b86b",
                                            "course__id": "41a50119-02b3-47bd-acff-6392e7d823ab",
                                            "course__name": "Cloud Engineering 2",
                                            "course__unit": 3,
                                            "registered_status": True,
                                        },
                                        {
                                            "id": "4a09baed-3a2d-4400-9fd9-09092c515941",
                                            "course__id": "d5f59de7-9a39-4c04-a910-cf36d89df89d",
                                            "course__name": "Computer Science 3",
                                            "course__unit": 3,
                                            "registered_status": True,
                                        },
                                    ],
                                    "total_units": 16,
                                },
                                "2024/2025 Academic Session 100LHarmattan": {
                                    "courses": [],
                                    "total_units": 0,
                                },
                                "2023/2024 Academic Session 100LHarmattan": {
                                    "courses": [],
                                    "total_units": 0,
                                },
                                "2023/2024 Academic Session 100LRain": {
                                    "courses": [],
                                    "total_units": 0,
                                },
                            },
                        },
                    ),
                ],
            ),
        },
    )


def live_result_docs():
    return extend_schema(
        summary="Retrieve live result",
        description="""
        This endpoint allows an authenticated user to retrieve live result
        """,
        tags=["Portal"],
        parameters=[
            OpenApiParameter(
                "semester", OpenApiTypes.STR, description="Semester ID", required=True
            ),
            OpenApiParameter(
                "level", OpenApiTypes.STR, description="Level ID", required=True
            ),
        ],
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Retrieved successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Retrieved successfully",
                            "data": {
                                "current_semester": {
                                    "total_units": 16,
                                    "total_points": 72,
                                    "gpa": 4.5,
                                    "grade_class": "First Class",
                                    "course_registrations": [
                                        {
                                            "course_code": "CSC101",
                                            "course_name": "Computer Science 1",
                                            "course_unit": 5,
                                            "course_exam_score": 74,
                                            "course_grade": "A",
                                            "course_points": 25,
                                        },
                                        {
                                            "course_code": "CSC102",
                                            "course_name": "Computer Science 2",
                                            "course_unit": 2,
                                            "course_exam_score": 65,
                                            "course_grade": "B",
                                            "course_points": 8,
                                        },
                                        {
                                            "course_code": "CLE104",
                                            "course_name": "Cloud Engineering",
                                            "course_unit": 3,
                                            "course_exam_score": 88,
                                            "course_grade": "A",
                                            "course_points": 15,
                                        },
                                        {
                                            "course_code": "CLE105",
                                            "course_name": "Cloud Engineering 2",
                                            "course_unit": 3,
                                            "course_exam_score": 82,
                                            "course_grade": "A",
                                            "course_points": 15,
                                        },
                                        {
                                            "course_code": "CSC103",
                                            "course_name": "Computer Science 3",
                                            "course_unit": 3,
                                            "course_exam_score": 59,
                                            "course_grade": "C",
                                            "course_points": 9,
                                        },
                                    ],
                                },
                                "cumulative_semesters": {
                                    "total_units": 16,
                                    "total_points": 72,
                                    "cgpa": 4.5,
                                    "grade_class": "First Class",
                                },
                            },
                        },
                    ),
                ],
            ),
        },
    )


def dashboard_docs():
    return extend_schema(
        summary="Retrieve dashboard",
        description="""
        This endpoint allows an authenticated user to retrieve dashboard
        """,
        tags=["Portal"],
        responses={
            200: OpenApiResponse(
                response={"application/json"},
                description="Retrieved successfully",
                examples=[
                    OpenApiExample(
                        name="Success response",
                        value={
                            "status": "success",
                            "message": "Retrieved successfully",
                            "data": {
                                "num_of_all_registered_courses": 5,
                                "cumulative_gpa": 4.5,
                                "total_num_of_carryovers": 0,
                                "total_units": 0,
                            },
                        },
                    ),
                ],
            ),
        },
    )
