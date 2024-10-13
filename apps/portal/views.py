from django.db import transaction
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.errors import ErrorCode
from apps.common.exceptions import RequestError
from apps.common.responses import CustomResponse
from apps.core.models import Level
from apps.portal.docs.docs import *
from apps.portal.models import Semester, Session, Course, CourseRegistration, GradeLevel
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
    all_semesters = Semester.objects.select_related("session").values("id", "name")

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
                    "is_registered": course.course_registered_by_student(user_profile),
                }
            )

        return CustomResponse.success(
            message="Retrieved successfully", data=course_list
        )


class RegisterCoursesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterCourseSerializer

    @register_courses_docs()
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        student_profile = request.user.profile
        latest_semester = Semester.objects.latest()

        serializer = self.serializer_class(
            data=request.data,
            context={"request": request, "student_profile": student_profile},
        )
        serializer.is_valid(raise_exception=True)

        courses = serializer.validated_data.get("valid_courses")

        # Register each course for the student
        course_registrations = []
        for course in courses:
            course_registrations.append(
                CourseRegistration(
                    student=student_profile,
                    course=course,
                    registered_status=True,
                    semester=latest_semester,
                    level=student_profile.level,
                )
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

        latest_semester = Semester.objects.latest()

        # Retrieve registered courses for the student
        course_registrations = CourseRegistration.objects.select_related(
            "student", "course", "semester", "level"
        ).filter(
            student=student_profile,
            registered_status=True,
            semester=latest_semester,
            level=student_profile.level,
        )

        # Aggregate course units
        total_units = (
                course_registrations.values("course__unit").aggregate(
                    total_units=Sum("course__unit")
                )["total_units"]
                or 0
        )

        # Retrieve course details
        courses = course_registrations.values(
            "id",
            "course__id",
            "course__name",
            "course__course_code",
            "course__unit",
            "registered_status",
        )

        response_data = {"courses": list(courses), "total_units": total_units}

        return CustomResponse.success(
            message="Retrieved successfully", data=response_data
        )


class UnregisterCourseView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UnregisterCourseSerializer

    @unregister_course_docs()
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        student_profile = request.user.profile
        latest_semester = Semester.objects.latest()
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        course_id = serializer.validated_data.get("course_id")

        course_registration = CourseRegistration.objects.select_related(
            "student", "course", "semester", "level"
        ).get(
            student=student_profile,
            course__id=course_id,
            semester=latest_semester,
            level=student_profile.level,
        )
        course_registration.registered_status = False
        course_registration.save()

        return CustomResponse.success("Course unregistered successfully")


class RetrieveAllSemestersRegisteredCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    @retrieve_all_semesters_registered_courses_docs()
    def get(request, *args, **kwargs):
        student_profile = request.user.profile
        all_semesters = Semester.objects.order_by("created")

        registered_courses_by_semester = {}

        # Retrieve registered courses for all semesters
        for semester in all_semesters:
            course_registrations = CourseRegistration.objects.select_related(
                "student", "course", "semester"
            ).filter(
                student=student_profile,
                registered_status=True,
                semester=semester,
                level=student_profile.level,
            )

            # Aggregate course units
            total_units = (
                    course_registrations.values("course__unit").aggregate(
                        total_units=Sum("course__unit")
                    )["total_units"]
                    or 0
            )

            # Retrieve course details
            courses = list(
                course_registrations.values(
                    "id",
                    "course__id",
                    "course__name",
                    "course__unit",
                    "registered_status",
                )
            )

            # Add semester data to the dictionary
            registered_courses_by_semester[
                f"{semester.session.name} {student_profile.level}{semester.name}"
            ] = {
                "courses": courses,
                "total_units": total_units,
            }

        # Reverse the order of the dictionary
        registered_courses_by_semester = dict(
            reversed(list(registered_courses_by_semester.items()))
        )

        return CustomResponse.success(
            message="Retrieved successfully", data=registered_courses_by_semester
        )


class RetrieveLiveResultsView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def calculate_cumulative_courses(student_profile):
        cumulative_courses = CourseRegistration.objects.select_related(
            "student", "course", "semester", "level"
        ).filter(
            student=student_profile,
            registered_status=True,
        )

        # Cumulative calculations
        cumulative_total_units = sum(
            [course.course.unit for course in cumulative_courses]
        )

        cumulative_total_points = sum(
            [
                course.course.unit * course.course_grade.point
                for course in cumulative_courses
                if course.course_grade
            ]
        )

        cumulative_gpa = (
            cumulative_total_points / cumulative_total_units
            if cumulative_total_units > 0
            else 0
        )

        # Fetch the grade level for the cumulative GPA
        return cumulative_gpa, cumulative_total_points, cumulative_total_units

    @staticmethod
    def calculate_current_semester(courses, total_points, total_units):
        # Loop through each course registration to calculate total units and points
        course_registrations = []

        for course_registration in courses:
            course = course_registration.course
            course_grade = course_registration.course_grade

            # Add course units to total units
            total_units += course.unit

            # Calculate points for the course if a grade is available
            if course_grade:
                course_points = course_grade.point * course.unit
                total_points += course_points
            else:
                course_points = "Not graded yet"

            # Collect data for each course
            course_registrations.append(
                {
                    "course_code": course.course_code,
                    "course_name": course.name,
                    "course_unit": course.unit,
                    "course_exam_score": course_registration.exam_score,
                    "course_grade": course_grade.grade if course_grade else "No grade",
                    "course_points": course_points,
                }
            )

        try:
            gpa_calculation = total_points / total_units if total_points > 0 else 0
        except ZeroDivisionError:
            gpa_calculation = None

        try:
            grade_class = GradeLevel.objects.get(
                min_point__lte=gpa_calculation, max_point__gte=gpa_calculation
            )
        except GradeLevel.DoesNotExist:
            grade_class = "No class found"

        return (
            course_registrations,
            gpa_calculation,
            grade_class,
            total_points,
            total_units,
        )

    @staticmethod
    @live_result_docs()
    def get(request, *args, **kwargs):
        student_profile = request.user.profile
        level = request.query_params.get("level")
        semester = request.query_params.get("semester")

        # Retrieve registered courses for the student
        courses = CourseRegistration.objects.select_related(
            "student", "course", "semester", "level"
        ).filter(
            student=student_profile,
            registered_status=True,
            semester=semester,
            level=level,
        )

        # Initialize variables to store total units and total points
        total_units = 0
        total_points = 0

        if courses.exists():
            (
                course_registrations,
                gpa_calculation,
                grade_class,
                total_points,
                total_units,
            ) = RetrieveLiveResultsView.calculate_current_semester(
                courses, total_points, total_units
            )
            current_semester_data = {
                "total_units": total_units,
                "total_points": total_points,
                "gpa": gpa_calculation,
                "grade_class": (
                    grade_class.name if grade_class else "No grade class"  # noqa
                ),
                "course_registrations": course_registrations,
            }
        else:
            # If no courses are registered for the current semester
            current_semester_data = "No courses found for the current semester"

        # Retrieve cumulative courses for the student
        cumulative_gpa, cumulative_total_points, cumulative_total_units = (
            RetrieveLiveResultsView.calculate_cumulative_courses(student_profile)
        )

        if cumulative_total_units > 0:
            cumulative_grade_class = GradeLevel.objects.get(
                min_point__lte=cumulative_gpa, max_point__gte=cumulative_gpa
            )
            cumulative_semester_data = {
                "total_units": cumulative_total_units,
                "total_points": cumulative_total_points,
                "cgpa": cumulative_gpa,
                "grade_class": cumulative_grade_class.name,
            }
        else:
            # If no cumulative data is available
            cumulative_semester_data = "No cumulative data found"

            # Handle both current semester and cumulative data being absent
        if (
                current_semester_data == "No courses found for the current semester"
                and cumulative_semester_data == "No cumulative data found"
        ):
            return RequestError(
                err_code=ErrorCode.NON_EXISTENT,
                err_msg="No data found",
                status_code=404,
            )

        data = {
            "current_semester": current_semester_data,
            "cumulative_semesters": cumulative_semester_data,
        }

        return CustomResponse.success(message="Retrieved successfully", data=data)


class RetrieveDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    @dashboard_docs()
    def get(request, *args, **kwargs):
        student_profile = request.user.profile
        course_registrations = CourseRegistration.objects.select_related(
            "student", "course", "semester", "level"
        ).filter(student=student_profile, registered_status=True)

        num_of_all_registered_courses = course_registrations.count()
        total_num_of_carryovers = 0

        # Retrieve cumulative courses for the student
        cumulative_gpa, _, cumulative_total_units = (
            RetrieveLiveResultsView.calculate_cumulative_courses(student_profile)
        )

        # Calculate carryovers(using how many Fs were carried over)
        for course in course_registrations:
            if course.course_grade is not None and course.course_grade.grade == "F":
                total_num_of_carryovers += 1

        data = {
            "num_of_all_registered_courses": num_of_all_registered_courses,
            "cumulative_gpa": round(cumulative_gpa, 2) if cumulative_gpa else 0,
            "total_num_of_carryovers": total_num_of_carryovers,
            "total_units": cumulative_total_units,
        }

        return CustomResponse.success(message="Retrieved successfully", data=data)
