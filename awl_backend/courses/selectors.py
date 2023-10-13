from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import render

from courses.models import Course


# Create your views here.
class CourseSelector:
    @staticmethod
    def all() -> QuerySet[Course]:
        return Course.objects.all()

    @classmethod
    def publicated(cls) -> QuerySet[Course]:
        return cls.all().filter(is_public=True)

    @staticmethod
    def get_by_id(pk: UUID) -> Course:
        return Course.objects.get(id=pk)
