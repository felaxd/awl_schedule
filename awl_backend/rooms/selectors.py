from uuid import UUID

from django.db.models import QuerySet

from rooms.models import Room


# Create your views here.
class RoomSelector:
    @staticmethod
    def all() -> QuerySet[Room]:
        return Room.objects.all()

    @classmethod
    def publicated(cls) -> QuerySet[Room]:
        return cls.all().filter(is_public=True)

    @staticmethod
    def get_by_id(pk: UUID) -> Room:
        return Room.objects.get(id=pk)
