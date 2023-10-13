from datetime import date
from typing import Optional, List
from uuid import UUID

from django.db.models import QuerySet

from schedule.models import ScheduleBlock


class ScheduleBlockSelector:
    @staticmethod
    def all() -> QuerySet[ScheduleBlock]:
        return ScheduleBlock.objects.all()

    @classmethod
    def publicated(cls) -> QuerySet[ScheduleBlock]:
        return cls.all().filter(is_public=True)

    @classmethod
    def filtered(
        cls,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        groups: Optional[List[int]] = None,
        lecturers: Optional[List[UUID]] = None,
        rooms: Optional[List[UUID]] = None,
    ) -> QuerySet[ScheduleBlock]:
        qs = cls.publicated()
        if date_from:
            qs = qs.filter(start__date__gte=date_from)
        if date_to:
            qs = qs.filter(end__date__lte=date_to)
        if groups:
            qs = qs.filter(groups__in=groups)
        if lecturers:
            qs = qs.filter(lecturers__in=lecturers)
        if rooms:
            qs = qs.filter(rooms__in=rooms)
        return qs.distinct()

    @staticmethod
    def get_by_id(block_id: UUID) -> ScheduleBlock:
        return ScheduleBlock.objects.get(id=block_id)
