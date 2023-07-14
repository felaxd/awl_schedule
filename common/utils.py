from typing import Any

from django.contrib.admin.models import LogEntry, ACTION_FLAG_CHOICES
from django.contrib.admin.options import get_content_type_for_model

from users.models import User


DICT_ACTION_FLAG_CHOICES = dict(ACTION_FLAG_CHOICES)


def django_log_action(user: User, obj: Any, action_flag: int, change_message: Any = "") -> LogEntry:
    """Small util so we can save logs for objects that can be read in django admin history page."""
    return LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=get_content_type_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=obj.__str__(),
        action_flag=action_flag,
        change_message=change_message or DICT_ACTION_FLAG_CHOICES.get(action_flag, ""),
    )
