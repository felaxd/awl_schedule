from users.models import Group
from django.db import models
from common.models import BaseDatabaseModel, TimestampMixin
from courses.models import Course
from lecturers.models import Lecturer
from rooms.models import Room


# Create your models here.
class Schedule(BaseDatabaseModel, TimestampMixin):
    name = models.CharField(max_length=128)
    status = models.CharField(max_length=32, default="NEW")

    file = models.FileField(upload_to="schedule/uploads/")
    progress = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("-created_at",)


class ScheduleBlock(BaseDatabaseModel, TimestampMixin):
    course_name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name="schedule_blocks", null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    type = models.CharField(max_length=32)
    lecturers = models.ManyToManyField(
        Lecturer, related_name="schedule_blocks", through="LecturerScheduleBlockThrough", blank=True
    )
    groups = models.ManyToManyField(Group, related_name="schedule_blocks")
    rooms = models.ManyToManyField(Room, related_name="schedule_blocks", blank=True)

    def __str__(self) -> str:
        return f"{self.start.date()} / {self.course_name}"

    class Meta:
        ordering = ("-created_at", "start")


class LecturerScheduleBlockThrough(BaseDatabaseModel, TimestampMixin):
    schedule_block = models.ForeignKey(ScheduleBlock, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.lecturer}{f' / {self.room.name}' if self.room else ''}"
