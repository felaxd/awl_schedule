from dataclasses import dataclass
from typing import Dict, Any

from django.contrib.admin.models import CHANGE
from django.db import transaction

from common.utils import django_log_action
from users.models import User


@dataclass
class UserService:
    @staticmethod
    @transaction.atomic()
    def update_user(user: User, **kwargs: Dict[str, Any]) -> User:
        """Updates user details"""
        # serialize input so kwargs has only User object fields
        user_model_fields = [field.name for field in User._meta.fields]
        if kwargs := {k: kwargs[k] for k in user_model_fields if k in kwargs.keys()}:
            User.objects.filter(id=user.id).update(**kwargs)
            user.refresh_from_db()
            user.full_clean()

            changed = user.changed_fields
            if changed:
                change_message = [{"changed": {"fields": changed}}]
                django_log_action(user=user, obj=user, action_flag=CHANGE, change_message=change_message)
        return user
