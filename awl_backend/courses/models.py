from users.models import Group
from django.db import models

from common.models import BaseDatabaseModel, TimestampMixin, ModelDifferenceMixin
from lecturers.models import Lecturer


# Create your models here.
class Course(BaseDatabaseModel, TimestampMixin, ModelDifferenceMixin):
    name = models.CharField(max_length=128, blank=False)
    groups = models.ManyToManyField(Group, through="GroupCourseThrough", related_name="courses")
    lecturers = models.ManyToManyField(Lecturer, through="LecturerCourseThrough", related_name="courses")
    is_public = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class GroupCourseThrough(BaseDatabaseModel, TimestampMixin):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    lecture_hours = models.IntegerField(default=0)
    exercises_hours = models.IntegerField(default=0)
    laboratory_hours = models.IntegerField(default=0)
    seminary_hours = models.IntegerField(default=0)
    project_hours = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.group.name


class LecturerCourseThrough(BaseDatabaseModel, TimestampMixin):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    lecture_hours = models.IntegerField(default=0)
    exercises_hours = models.IntegerField(default=0)
    laboratory_hours = models.IntegerField(default=0)
    seminary_hours = models.IntegerField(default=0)
    project_hours = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.lecturer} / {self.group}"
