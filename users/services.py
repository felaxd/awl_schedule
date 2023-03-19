from dataclasses import dataclass
from typing import Dict, Any

from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.forms import model_to_dict

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
            pre_change_details = model_to_dict(user, fields=user_model_fields)
            User.objects.filter(id=user.id).update(**kwargs)
            user.refresh_from_db()
            user.full_clean()

            post_change_details = model_to_dict(user, fields=user_model_fields)
            changed = [field for field, value in pre_change_details.items() if value != post_change_details[field]]
            if changed:
                LogEntry.objects.log_action(
                    user_id=user.id,
                    content_type_id=ContentType.objects.get_for_model(user).pk,
                    object_id=user.pk,
                    object_repr=user.__str__(),
                    action_flag=CHANGE,
                    change_message=[{"changed": {"fields": changed}}],
                )
        return user
