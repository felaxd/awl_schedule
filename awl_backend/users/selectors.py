from uuid import UUID

from django.db.models import QuerySet

from users.models import Group

from users.models import User


class UserSelector:
    @staticmethod
    def get_by_id(pk: UUID) -> User:
        return User.objects.get(id=pk)


class GroupSelector:
    @staticmethod
    def all() -> QuerySet[Group]:
        return Group.objects.all()

    @classmethod
    def publicated(cls) -> QuerySet[Group]:
        return cls.all().filter(is_public=True)

    @staticmethod
    def get_by_id(pk: int) -> Group:
        return Group.objects.get(id=pk)
