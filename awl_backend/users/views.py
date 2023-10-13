from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.container import container
from users.selectors import GroupSelector
from users.serializers import UserDetailsSerializer, GroupSerializer


class UserDetailsView(GenericAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

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


class GroupListView(GenericAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request) -> Response:
        """Returns all groups"""
        groups = GroupSelector.publicated().order_by("name")
        return Response(self.get_serializer(groups, many=True).data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Creates new group"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = container().group_service.create_group(user=request.user, name=serializer.validated_data["name"])
        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)


class GroupDetailsView(GenericAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request, group_id: int) -> Response:
        """Returns single group details"""
        group = GroupSelector.get_by_id(group_id)
        return Response(self.get_serializer(group).data, status=status.HTTP_200_OK)

    def put(self, request: Request, group_id: int) -> Response:
        """Updates group details"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = container().group_service.update_group(request.user, group_id, name=serializer.validated_data["name"])
        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)

    def patch(self, request: Request, group_id: int) -> Response:
        """Partially updates group details"""
        serializer = self.get_serializer(data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = container().group_service.update_group(request.user, group_id, name=serializer.validated_data["name"])
        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)

    def delete(self, request: Request, group_id: int) -> Response:
        """Deletes group"""
        container().group_service.delete_group(request.user, group_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
