from dataclasses import dataclass
from typing import Dict, Any
from uuid import UUID

from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.db import transaction

from common.utils import django_log_action
from common.validators import validate_user_permission
from lecturers.models import Lecturer
from lecturers.selectors import LecturerSelector
from users.models import User


@dataclass
class LecturerService:
    @staticmethod
    @transaction.atomic()
    def create_lecturer(
        user: User,
        first_name: str,
        last_name: str,
        title: str = "",
        job_position: str = "",
        contact_email: str = ""
    ) -> Lecturer:
        """Creates lecturer details"""
        lecturer = Lecturer(
            first_name=first_name,
            last_name=last_name,
            title=title,
            job_position=job_position,
            contact_email=contact_email,
        )
        validate_user_permission(user, lecturer.ADD_PERMISSION_CODENAME, raise_error=True)
        lecturer.full_clean()
        lecturer.save()

        django_log_action(user=user, obj=lecturer, action_flag=ADDITION)
        return lecturer

    @staticmethod
    @transaction.atomic()
    def update_lecturer(user: User, lecturer_id: UUID, **kwargs: Dict[str, Any]) -> Lecturer:
        """Updates lecturer details"""
        lecturer = LecturerSelector.get_by_id(lecturer_id)
        validate_user_permission(user, lecturer.CHANGE_PERMISSION_CODENAME, raise_error=True)

        # serialize input so kwargs has only Lecturer object fields
        model_fields = [field.name for field in Lecturer._meta.fields]
        if kwargs := {k: kwargs[k] for k in model_fields if k in kwargs.keys()}:
            Lecturer.objects.filter(id=lecturer.id).update(**kwargs)
            lecturer.refresh_from_db()
            lecturer.full_clean()

            changed = lecturer.changed_fields
            if changed:
                change_message = [{"changed": {"fields": changed}}]
                django_log_action(user=user, obj=lecturer, action_flag=CHANGE, change_message=change_message)
        return lecturer

    @staticmethod
    @transaction.atomic()
    def delete_lecturer(user: User, lecturer_id: UUID) -> None:
        lecturer = LecturerSelector.get_by_id(lecturer_id)
        validate_user_permission(user, lecturer.DELETE_PERMISSION_CODENAME, raise_error=True)
        lecturer.delete()

        django_log_action(user=user, obj=lecturer, action_flag=DELETION)
        return None
