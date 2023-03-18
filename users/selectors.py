from uuid import UUID

from users.models import User


class UserSelector:
    @staticmethod
    def get_by_id(pk: UUID) -> User:
        return User.objects.get(id=pk)
