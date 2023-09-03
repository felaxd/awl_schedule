from uuid import UUID

from django.db.models import QuerySet

from schedule.models import ScheduleBlock


class ScheduleBlockSelector:
    @staticmethod
    def all() -> QuerySet[ScheduleBlock]:
        return ScheduleBlock.objects.all()

    @staticmethod
    def get_by_id(block_id: UUID) -> ScheduleBlock:
        return ScheduleBlock.objects.get(id=block_id)
