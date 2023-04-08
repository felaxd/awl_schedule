from uuid import UUID

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from common.container import container
from rooms.selectors import RoomSelector
from rooms.serializers import RoomSerializer


# Create your views here.
class RoomListView(GenericAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request) -> Response:
        """Returns all rooms"""
        groups = RoomSelector.all()
        return Response(self.get_serializer(groups, many=True).data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Creates new room"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = container().room_service.create_room(user=request.user, name=serializer.validated_data["name"])
        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)


class RoomDetailsView(GenericAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request, room_id: UUID) -> Response:
        """Returns single room details"""
        group = RoomSelector.get_by_id(room_id)
        return Response(self.get_serializer(group).data, status=status.HTTP_200_OK)

    def delete(self, request: Request, room_id: UUID) -> Response:
        """Deletes room"""
        container().room_service.delete_room(request.user, room_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
