from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class NoAuthMixin:
    permission_classes = []
    authentication_classes = []


class AuthMixin:
    """Ensures user is authenticated when accessing view"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
