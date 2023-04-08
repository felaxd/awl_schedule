from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import render

from courses.models import Course


# Create your views here.
class CourseSelector:
    @staticmethod
    def all() -> QuerySet[Course]:
        return Course.objects.all()

    @staticmethod
    def get_by_id(pk: UUID) -> Course:
        return Course.objects.get(id=pk)
