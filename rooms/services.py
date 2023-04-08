from dataclasses import dataclass
from uuid import UUID

from django.contrib.admin.models import ADDITION, DELETION
from django.db import transaction

from common.utils import django_log_action
from common.validators import validate_user_permission
from rooms.models import Room
from rooms.selectors import RoomSelector
from users.models import User


# Create your views here.
@dataclass
class RoomService:
    @staticmethod
    @transaction.atomic()
    def create_room(user: User, name: str) -> Room:
        room = Room(name=name)
        validate_user_permission(user, room.ADD_PERMISSION_CODENAME, raise_error=True)
        room.full_clean()
        room.save()

        django_log_action(user=user, obj=room, action_flag=ADDITION)
        return room

    @staticmethod
    @transaction.atomic()
    def delete_room(user: User, room_id: UUID) -> None:
        room = RoomSelector.get_by_id(room_id)
        validate_user_permission(user, room.DELETE_PERMISSION_CODENAME, raise_error=True)
        room.delete()

        django_log_action(user=user, obj=room, action_flag=DELETION)
        return None
