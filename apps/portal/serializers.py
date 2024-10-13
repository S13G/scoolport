from rest_framework import serializers

from apps.portal.models import Course, CourseRegistration, Semester


class RegisterCourseSerializer(serializers.Serializer):
    courses_id = serializers.ListField(child=serializers.CharField())

    def validate(self, attrs):
        courses_id = attrs.get("courses_id", [])
        latest_semester = Semester.objects.latest()

        level = self.context["student_profile"].level

        # Validate course list
        if not courses_id:
            raise serializers.ValidationError("Course list cannot be empty.")

        # Check for duplicate IDs
        if len(courses_id) != len(set(courses_id)):
            raise serializers.ValidationError("Duplicate course IDs are not allowed.")

        # Fetch courses in bulk to minimize database queries
        courses = Course.objects.filter(id__in=courses_id)

        # Check if any courses do not exist and if their semester matches the latest semester
        valid_courses = []
        valid_courses_unit = []

        for course_id in courses_id:
            try:
                course = courses.get(id=course_id)

                valid_courses.append(course)
                valid_courses_unit.append(course.unit)

            except Course.DoesNotExist:
                raise serializers.ValidationError(
                    f"Course with ID {course_id} does not exist."
                )

        # Check if the user is already registered for any of the courses
        if (
            CourseRegistration.objects.select_related(
                "student", "course", "semester", "level"
            )
            .filter(
                student=self.context["request"].user.profile,
                course__id__in=courses_id,
                semester=latest_semester,
                level=level,
            )
            .exists()
        ):
            raise serializers.ValidationError("A course is already registered.")

        # Checking if total units registered exceeds 24
        total_units = sum(valid_courses_unit)
        if total_units > 24:
            raise serializers.ValidationError(
                "Total units of courses to register cannot exceed 24."
            )

        attrs["valid_courses"] = valid_courses
        return attrs


class UnregisterCourseSerializer(serializers.Serializer):
    course_id = serializers.CharField()

    def validate(self, attrs):
        course_id = attrs.get("course_id", None)
        latest_semester = Semester.objects.latest()
        level = self.context["student_profile"].level

        # Check if course exists
        if not Course.objects.filter(id=course_id).exists():
            raise serializers.ValidationError("Course not found.")

        # Check if course is already unregistered
        if (
            CourseRegistration.objects.select_related(
                "student", "course", "semester", "level"
            )
            .filter(
                student=self.context["student_profile"],
                course__id=course_id,
                semester=latest_semester,
                level=level,
                registered_status=False,
            )
            .exists()
        ):
            raise serializers.ValidationError("Course already unregistered.")

        return attrs
