from typing import Union, Type
from uuid import UUID

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from common.container import container
from lecturers.selectors import LecturerSelector
from lecturers.serializers import LecturerSerializer, LecturerDetailSerializer


class LecturerListView(GenericAPIView):
    serializer_class = LecturerSerializer
    create_serializer_class = LecturerDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self) -> Union[Type[LecturerSerializer], Type[LecturerDetailSerializer]]:
        if self.request.method == "POST":
            return self.create_serializer_class
        return self.serializer_class

    def get(self, request: Request) -> Response:
        """Returns list of lecturers"""
        result = LecturerSelector.publicated().order_by("last_name")
        return Response(self.get_serializer(result, many=True).data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Updates single lecturer details"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        lecturer = container().lecturer_service.create_lecturer(request.user, **serializer.validated_data)
        return Response(self.get_serializer(lecturer).data, status=status.HTTP_201_CREATED)


class LecturerDetailsView(GenericAPIView):
    serializer_class = LecturerSerializer
    authenticated_serializer_class = LecturerDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self) -> Union[Type[LecturerSerializer], Type[LecturerDetailSerializer]]:
        if self.request.user.is_authenticated:
            return self.authenticated_serializer_class
        return self.serializer_class

    def get(self, request: Request, lecturer_id: UUID) -> Response:
        """Returns single lecturer details"""
        result = LecturerSelector.get_by_id(lecturer_id)
        return Response(self.get_serializer(result).data, status=status.HTTP_200_OK)

    def put(self, request: Request, lecturer_id: UUID) -> Response:
        """Updates single lecturer details"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        lecturer = container().lecturer_service.update_lecturer(request.user, lecturer_id, **serializer.validated_data)
        return Response(self.get_serializer(lecturer).data, status=status.HTTP_200_OK)

    def patch(self, request: Request, lecturer_id: UUID) -> Response:
        """Partially updates single lecturer details"""
        serializer = self.get_serializer(data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        lecturer = container().lecturer_service.update_lecturer(request.user, lecturer_id, **serializer.validated_data)
        return Response(self.get_serializer(lecturer).data, status=status.HTTP_200_OK)

    def delete(self, request: Request, lecturer_id: UUID) -> Response:
        """Deletes lecturer"""

        serializer = self.get_serializer(data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        container().lecturer_service.delete_lecturer(request.user, lecturer_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
