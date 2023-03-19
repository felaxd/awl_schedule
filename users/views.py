from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.container import container
from users.serializers import UserDetailsSerializer


class UserDetailsView(GenericAPIView):
    serializer_class = UserDetailsSerializer

    def get(self, request: Request) -> Response:
        """Returns logged in user details"""
        return Response(self.get_serializer(request.user).data, status=status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        """Updates user details"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = container().user_service.update_user(request.user, **serializer.validated_data)
        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)

    def patch(self, request: Request) -> Response:
        """Partially updates user details"""
        serializer = self.get_serializer(data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = container().user_service.update_user(request.user, **serializer.validated_data)
        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)
