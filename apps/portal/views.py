from django.db import transaction
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.responses import CustomResponse
from apps.core.models import Level
from apps.portal.docs.docs import *
from apps.portal.models import Semester, Session, Course, CourseRegistration
from apps.portal.serializers import RegisterCourseSerializer, UnregisterCourseSerializer


# Create your views here.
@retrieve_session_docs()
class RetrieveSessionView(APIView):
    permission_classes = [IsAuthenticated]
    all_sessions = Session.objects.values("id", "name")

    def get(self, request):
        data = list(self.all_sessions)
        return CustomResponse.success(message="Retrieved successfully", data=data)


@retrieve_semester_docs()
class RetrieveSemestersView(APIView):
    all_semesters = Semester.objects.select_related('session').values("id", "name")

    def get(self, request, *args, **kwargs):
        session_id = self.kwargs.get("session_id")
        self.all_semesters = self.all_semesters.filter(session__id=session_id)

        data = list(self.all_semesters)
        return CustomResponse.success(message="Retrieved successfully", data=data)


class RetrieveLevelsView(APIView):
    all_levels = Level.objects.values("id", "name")

    @retrieve_level_docs()
    def get(self, request):
        data = list(self.all_levels)
        return CustomResponse.success(message="Retrieved successfully", data=data)


class RetrieveCoursesToRegisterView(APIView):

    @staticmethod
    def filter_courses(courses, level, search, semester):
        # Apply semester filter only if a valid value is provided
        if semester:
            courses = courses.filter(semester__id=semester)
        # Apply level filter only if a valid value is provided
        if level:
            courses = courses.filter(course_level__id=level)
        # Apply search filter if provided
        if search:
            courses = courses.filter(course_code__icontains=search)
        return courses

    @retrieve_courses_to_register_docs()
    def get(self, request, *args, **kwargs):
        user_profile = request.user.profile
        user_department = user_profile.department
        semester = request.query_params.get("semester", None)
        level = request.query_params.get("level", None)
        search = request.query_params.get("search", None)

        # Get the list of courses for the department
        courses = Course.objects.filter(department=user_department)

        # Apply filters based on query params
        courses = self.filter_courses(courses, level, search, semester)

        # Prepare the result with course registration status
        course_list = []
        for course in courses:
            course_list.append(
                {
                    "id": course.id,
                    "name": course.name,
                    "course_code": course.course_code,
                    "unit": course.unit,
                    "is_registered": course.course_registered_by_student(user_profile)
                }
            )

        return CustomResponse.success(message="Retrieved successfully", data=course_list)


class RegisterCoursesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterCourseSerializer

    @register_courses_docs()
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        student_profile = request.user.profile
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        courses = serializer.validated_data.get("valid_courses")

        # Register each course for the student
        course_registrations = []
        for course in courses:
            course_registrations.append(
                CourseRegistration(student=student_profile, course=course, registered_status=True)
            )

        # Bulk create CourseRegistration objects
        if course_registrations:
            CourseRegistration.objects.bulk_create(course_registrations)

        return CustomResponse.success(message="Registered successfully")


class RetrieveRegisteredCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    @retrieve_registered_courses_docs()
    def get(request, *args, **kwargs):
        student_profile = request.user.profile

        # Retrieve registered courses for the student
        course_registrations = (
            CourseRegistration.objects.select_related("student", "course")
            .filter(student=student_profile, registered_status=True)
        )

        # Aggregate course units
        total_units = (
                course_registrations.values('course__unit')
                .aggregate(total_units=Sum('course__unit'))[
                    'total_units'] or 0
        )

        # Retrieve course details
        courses = course_registrations.values("id", "course__id", "course__name", "course__unit", "registered_status")

        response_data = {
            "courses": list(courses),
            "total_units": total_units
        }

        return CustomResponse.success(message="Retrieved successfully", data=response_data)


class UnregisterCourseView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UnregisterCourseSerializer

    @unregister_course_docs()
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        student_profile = request.user.profile
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        course_id = serializer.validated_data.get("course_id")

        course_registration = CourseRegistration.objects.select_related("student", "course").get(
            student=student_profile, course__id=course_id)
        course_registration.registered_status = False
        course_registration.save()

        return CustomResponse.success("Course unregistered successfully")
