from django.core.exceptions import PermissionDenied

from users.models import User


def validate_user_permission(user: User, perm_code: str, raise_error: bool = False) -> bool:
    """Checks if user has specific permission assigned. Can raise `PermissionDenied` if raise_error is True"""
    has_perm = user.has_perm(perm_code)
    if raise_error and not has_perm:
        raise PermissionDenied
    return has_perm
