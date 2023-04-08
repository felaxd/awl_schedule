from dataclasses import dataclass
from typing import Dict, Any

from django.contrib.admin.models import CHANGE, ADDITION
from django.db import transaction

from common.utils import django_log_action
from common.validators import validate_user_permission
from users.models import User, Group
from users.selectors import GroupSelector


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


@dataclass
class GroupService:
    @staticmethod
    @transaction.atomic()
    def create_group(user: User, name: str) -> Group:
        group = Group(name=name)
        validate_user_permission(user, group.ADD_PERMISSION_CODENAME, raise_error=True)
        group.full_clean()
        group.save()

        django_log_action(user=user, obj=group, action_flag=ADDITION)
        return group

    @staticmethod
    @transaction.atomic()
    def update_group(user: User, group_id: int, name: str) -> Group:
        group = GroupSelector.get_by_id(group_id)
        validate_user_permission(user, group.CHANGE_PERMISSION_CODENAME, raise_error=True)

        Group.objects.filter(id=group.id).update(name=name)
        group.refresh_from_db()
        group.full_clean()

        changed = group.changed_fields
        if changed:
            change_message = [{"changed": {"fields": changed}}]
            django_log_action(user=user, obj=group, action_flag=CHANGE, change_message=change_message)
        return group

    @staticmethod
    @transaction.atomic()
    def delete_group(user: User, group_id: int) -> None:
        group = GroupSelector.get_by_id(group_id)
        validate_user_permission(user, group.DELETE_PERMISSION_CODENAME, raise_error=True)
        group.delete()
        return None
