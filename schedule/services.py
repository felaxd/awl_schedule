from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from uuid import UUID

from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.core.exceptions import ValidationError
from django.db import transaction

from common.utils import django_log_action
from common.validators import validate_user_permission
from courses.models import Course
from lecturers.models import Lecturer
from rooms.models import Room
from schedule.models import ScheduleBlock
from schedule.selectors import ScheduleBlockSelector
from users.models import User, Group


@dataclass
class ScheduleBlockService:

    @staticmethod
    @transaction.atomic()
    def set_schedule_block_lecturers(
        user: User, schedule_block: ScheduleBlock, lecturers: List[Dict[str, Union[Lecturer, Room]]]
    ) -> None:
        schedule_block.lecturers.clear()
        for lecturer in lecturers:
            _lecturer = lecturer.get("lecturer")
            schedule_block.lecturers.add(_lecturer, through_defaults={"room": lecturer.get("room", None)})

        change_message = f"Changed lecturers ({', '.join([l.__str__() for l in schedule_block.lecturers.all()])})"
        django_log_action(user=user, obj=schedule_block, action_flag=CHANGE, change_message=change_message)

    @staticmethod
    @transaction.atomic()
    def set_schedule_block_groups(user: User, schedule_block: ScheduleBlock, groups: List[Group]) -> None:
        schedule_block.groups.clear()
        for group in groups:
            schedule_block.groups.add(group)
        change_message = f"Changed groups ({', '.join(schedule_block.groups.values_list('name', flat=True))})"
        django_log_action(user=user, obj=schedule_block, action_flag=CHANGE, change_message=change_message)

    @staticmethod
    @transaction.atomic()
    def set_schedule_block_rooms(user: User, schedule_block: ScheduleBlock, rooms: List[Room]) -> None:
        schedule_block.rooms.clear()
        for room in rooms:
            schedule_block.rooms.add(room)
        change_message = f"Changed rooms ({', '.join(schedule_block.rooms.values_list('name', flat=True))})"
        django_log_action(user=user, obj=schedule_block, action_flag=CHANGE, change_message=change_message)

    @transaction.atomic()
    def create_schedule_block(
        self,
        user: User,
        course_name: str,
        course: Optional[Course],
        start: datetime,
        end: datetime,
        type: str,
        lecturers: Optional[List[Dict[str, Union[Lecturer, Room]]]] = None,
        groups: Optional[List[Group]] = None,
        rooms: Optional[List[Room]] = None
    ) -> ScheduleBlock:
        """Creates schedule block"""
        schedule_block = ScheduleBlock(
            course_name=course_name,
            course=course,
            start=start,
            end=end,
            type=type,
        )
        validate_user_permission(user, schedule_block.ADD_PERMISSION_CODENAME, raise_error=True)
        schedule_block.full_clean()
        schedule_block.save()

        django_log_action(user=user, obj=schedule_block, action_flag=ADDITION)

        if lecturers:
            self.set_schedule_block_lecturers(user, schedule_block, lecturers)

        if groups:
            self.set_schedule_block_groups(user, schedule_block, groups)
        else:
            raise ValidationError({"groups": "Lista nie może być pusta."})

        if rooms:
            self.set_schedule_block_rooms(user, schedule_block, rooms)

        return schedule_block

    @transaction.atomic()
    def update_schedule_block(self, user: User, schedule_block_id: UUID, **kwargs: Dict[str, Any]) -> ScheduleBlock:
        """Updates schedule block details"""
        schedule_block = ScheduleBlockSelector.get_by_id(schedule_block_id)
        validate_user_permission(user, schedule_block.CHANGE_PERMISSION_CODENAME, raise_error=True)

        lecturers: Optional[List[Dict[str, Union[Lecturer, Room]]]] = kwargs.pop("lecturers", None)
        groups: Optional[List[Group]] = kwargs.pop("groups", None)
        rooms: Optional[List[Room]] = kwargs.pop("rooms", None)

        # serialize input so kwargs has only Lecturer object fields
        model_fields = [field.name for field in ScheduleBlock._meta.fields]
        if kwargs := {k: kwargs[k] for k in model_fields if k in kwargs.keys()}:
            ScheduleBlock.objects.filter(id=schedule_block.id).update(**kwargs)
            schedule_block.refresh_from_db()
            schedule_block.full_clean()

            changed = schedule_block.changed_fields
            if changed:
                change_message = [{"changed": {"fields": changed}}]
                django_log_action(user=user, obj=schedule_block, action_flag=CHANGE, change_message=change_message)

        if lecturers is not None:
            self.set_schedule_block_lecturers(user, schedule_block, lecturers)

        if groups is not None:
            self.set_schedule_block_groups(user, schedule_block, groups)

        if rooms is not None:
            self.set_schedule_block_rooms(user, schedule_block, rooms)

        return schedule_block

    @staticmethod
    @transaction.atomic()
    def delete_schedule_block(user: User, schedule_block_id: UUID) -> None:
        schedule_block = ScheduleBlockSelector.get_by_id(schedule_block_id)
        validate_user_permission(user, schedule_block.DELETE_PERMISSION_CODENAME, raise_error=True)
        schedule_block.delete()

        django_log_action(user=user, obj=schedule_block, action_flag=DELETION)
        return None
