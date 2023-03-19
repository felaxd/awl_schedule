from rest_framework import serializers

from lecturers.models import Lecturer


# Create your views here.
class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = (
            "id",
            "first_name",
            "last_name",
            "title",
            "contact_email",
        )


class LecturerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = (
            "id",
            "first_name",
            "last_name",
            "title",
            "job_position",
            "contact_email",
        )
