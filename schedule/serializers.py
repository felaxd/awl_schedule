from rest_framework import serializers

from lecturers.models import Lecturer
from lecturers.serializers import LecturerSerializer
from rooms.serializers import RoomSerializer
from schedule.models import ScheduleBlock, LecturerScheduleBlockThrough
from users.serializers import GroupSerializer


class ScheduleBlockLecturerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerScheduleBlockThrough
        fields = (
            "lecturer",
            "room",
        )


class ScheduleBlockLecturerSerializer(ScheduleBlockLecturerCreateSerializer):
    lecturer = LecturerSerializer(read_only=True)
    room = RoomSerializer(read_only=True)


class ScheduleBlockSerializer(serializers.ModelSerializer):
    lecturers = ScheduleBlockLecturerSerializer(source="lecturerscheduleblockthrough_set", read_only=True, many=True)
    groups = GroupSerializer(read_only=True, many=True)
    rooms = RoomSerializer(read_only=True, many=True)

    class Meta:
        model = ScheduleBlock
        fields = (
            "id",
            "course_name",
            "course",
            "start",
            "end",
            "type",
            "lecturers",
            "groups",
            "rooms",
        )


class ScheduleBlockCreateSerializer(serializers.ModelSerializer):
    lecturers = ScheduleBlockLecturerCreateSerializer(many=True)

    class Meta:
        model = ScheduleBlock
        fields = (
            "id",
            "course_name",
            "course",
            "start",
            "end",
            "type",
            "lecturers",
            "groups",
            "rooms",
        )
