from rest_framework import serializers

from courses.models import Course, GroupCourseThrough, LecturerCourseThrough
from lecturers.serializers import LecturerSerializer
from users.serializers import GroupSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "name",
        )


class CourseDetailSerializer(serializers.ModelSerializer):
    lecturers = LecturerSerializer(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "groups",
            "lecturers",
        )


class CourseGroupRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupCourseThrough
        fields = (
            "lecture_hours",
            "exercises_hours",
            "laboratory_hours",
            "seminary_hours",
            "project_hours",
        )
        extra_kwargs = {
            "lecture_hours": {"required": False},
            "exercises_hours": {"required": False},
            "laboratory_hours": {"required": False},
            "seminary_hours": {"required": False},
            "project_hours": {"required": False},
        }


class CourseLecturerRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerCourseThrough
        fields = (
            "group",
            "lecture_hours",
            "exercises_hours",
            "laboratory_hours",
            "seminary_hours",
            "project_hours",
        )
        extra_kwargs = {
            "lecture_hours": {"required": False},
            "exercises_hours": {"required": False},
            "laboratory_hours": {"required": False},
            "seminary_hours": {"required": False},
            "project_hours": {"required": False},
        }
