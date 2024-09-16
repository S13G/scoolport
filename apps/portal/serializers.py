from rest_framework import serializers

from apps.portal.models import Course, CourseRegistration


class RegisterCourseSerializer(serializers.Serializer):
    courses_id = serializers.ListField(child=serializers.CharField())

    def validate(self, attrs):
        courses_id = attrs.get('courses_id', [])

        if not courses_id:
            raise serializers.ValidationError("Course list cannot be empty.")

        # Check for duplicate IDs
        if len(courses_id) != len(set(courses_id)):
            raise serializers.ValidationError("Duplicate course IDs are not allowed.")

        # Check if course is already registered
        if CourseRegistration.objects.filter(student=self.context['request'].user.profile,
                                             course__id__in=courses_id).exists():
            raise serializers.ValidationError("A course is already registered.")

        # Initialize an empty list to store validated course unit
        valid_courses = []
        valid_courses_unit = []

        # Loop through the course IDs and check if they exist in the database
        for course_id in courses_id:
            try:
                course = Course.objects.get(id=course_id)
                valid_courses.append(course)
                valid_courses_unit.append(course.unit)
            except Course.DoesNotExist:
                raise serializers.ValidationError(f"Course with ID {course_id} does not exist.")

        # Checking if total courses registered is more than 24
        total_units = sum(valid_courses_unit)
        if total_units > 24:
            raise serializers.ValidationError("Total units of courses to register cannot exceed 24.")

        attrs['valid_courses'] = valid_courses
        return attrs


class UnregisterCourseSerializer(serializers.Serializer):
    course_id = serializers.CharField()

    def validate(self, attrs):
        course_id = attrs.get('course_id', None)

        if not Course.objects.filter(id=course_id).exists():
            raise serializers.ValidationError("Course not found.")

        if not CourseRegistration.objects.filter(student=self.context['request'].user.profile,
                                                 course__id=course_id).exists():
            raise serializers.ValidationError("Course not registered.")

        return attrs
