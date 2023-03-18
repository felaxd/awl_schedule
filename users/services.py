from dataclasses import dataclass

from django.db import transaction

from users.models import User


@dataclass
class UserService:
    @staticmethod
    @transaction.atomic()
    def update_user(user: User, **kwargs) -> User:
        """Updates user details"""
        User.objects.filter(id=user.id).update(**kwargs)
        user.refresh_from_db()
        user.full_clean()
        return user
