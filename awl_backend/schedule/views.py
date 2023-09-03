from typing import Union, Type
from uuid import UUID

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from common.container import container
from schedule.selectors import ScheduleBlockSelector
from schedule.serializers import ScheduleBlockSerializer, ScheduleBlockCreateSerializer


class ScheduleBlockListView(GenericAPIView):
    serializer_class = ScheduleBlockSerializer
    create_serializer_class = ScheduleBlockCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self) -> Union[Type[ScheduleBlockSerializer], Type[ScheduleBlockCreateSerializer]]:
        if self.request.method == "POST":
            return self.create_serializer_class
        return self.serializer_class

    def get(self, request: Request) -> Response:
        """Returns list of schedule blocks"""
        result = ScheduleBlockSelector.all()
        return Response(self.get_serializer(result, many=True).data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Creates single schedule block"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        schedule_block = container().schedule_block_service.create_schedule_block(
            request.user, **serializer.validated_data
        )
        return Response(self.serializer_class(schedule_block).data, status=status.HTTP_201_CREATED)


class ScheduleBlockDetailsView(GenericAPIView):
    serializer_class = ScheduleBlockSerializer
    update_serializer_class = ScheduleBlockCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self) -> Union[Type[ScheduleBlockSerializer], Type[ScheduleBlockCreateSerializer]]:
        if self.request.method in ["PUT", "PATCH"]:
            return self.update_serializer_class
        return self.serializer_class

    def get(self, request: Request, schedule_block_id: UUID) -> Response:
        """Returns single schedule block details"""
        result = ScheduleBlockSelector.get_by_id(schedule_block_id)
        return Response(self.get_serializer(result).data, status=status.HTTP_200_OK)

    def put(self, request: Request, schedule_block_id: UUID) -> Response:
        """Updates single schedule block details"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        schedule_block = container().schedule_block_service.update_schedule_block(
            request.user, schedule_block_id, **serializer.validated_data
        )
        return Response(self.serializer_class(schedule_block).data, status=status.HTTP_200_OK)

    def patch(self, request: Request, schedule_block_id: UUID) -> Response:
        """Partially updates single schedule block details"""
        serializer = self.get_serializer(data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        schedule_block = container().schedule_block_service.update_schedule_block(
            request.user, schedule_block_id, **serializer.validated_data
        )
        return Response(self.serializer_class(schedule_block).data, status=status.HTTP_200_OK)

    def delete(self, request: Request, schedule_block_id: UUID) -> Response:
        """Deletes schedule block"""

        serializer = self.get_serializer(data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        container().schedule_block_service.delete_schedule_block(request.user, schedule_block_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
