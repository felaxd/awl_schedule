from django.utils import timezone

from users.models import Group, User
from django.db import models
from common.models import BaseDatabaseModel, TimestampMixin, ModelDifferenceMixin
from courses.models import Course
from lecturers.models import Lecturer
from rooms.models import Room


# Create your models here.
class Schedule(BaseDatabaseModel, TimestampMixin):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")
    name = models.CharField(max_length=128)
    status = models.CharField(max_length=32, default="NEW")

    file = models.FileField(upload_to="schedule/uploads/")
    year = models.IntegerField(default=timezone.now().year, blank=False)
    month = models.IntegerField(default=timezone.now().month, blank=False)
    worksheet_name = models.CharField(max_length=128, blank=False)
    progress = models.IntegerField(blank=True, default=0)

    errors = models.JSONField(default=list, blank=True)
    schedule_blocks = models.ManyToManyField("ScheduleBlock", blank=True, related_name="schedules")
    lecturers = models.ManyToManyField(Lecturer, blank=True, related_name="schedules")
    groups = models.ManyToManyField(Group, blank=True, related_name="schedules")
    rooms = models.ManyToManyField(Room, blank=True, related_name="schedules")
    courses = models.ManyToManyField(Course, blank=True, related_name="schedules")

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("-created_at",)


class ScheduleBlock(BaseDatabaseModel, TimestampMixin, ModelDifferenceMixin):
    is_public = models.BooleanField(default=False)
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
        return f"{self.start.strftime('%d/%m/%Y %H:%M')} / {self.course_name}"

    class Meta:
        ordering = ("-created_at", "start")


class LecturerScheduleBlockThrough(BaseDatabaseModel, TimestampMixin):
    schedule_block = models.ForeignKey(ScheduleBlock, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.lecturer}{f' / {self.room.name}' if self.room else ''}"
