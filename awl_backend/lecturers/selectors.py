from uuid import UUID

from django.db.models import QuerySet

from lecturers.models import Lecturer


# Create your views here.
class LecturerSelector:
    @staticmethod
    def all() -> QuerySet[Lecturer]:
        return Lecturer.objects.all()

    @classmethod
    def publicated(cls) -> QuerySet[Lecturer]:
        return cls.all().filter(is_public=True)

    @staticmethod
    def get_by_id(pk: UUID) -> Lecturer:
        return Lecturer.objects.get(id=pk)
