from uuid import UUID

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.container import container
from courses.selectors import CourseSelector
from courses.serializers import CourseSerializer, CourseDetailSerializer, CourseGroupRelationSerializer, \
    CourseLecturerRelationSerializer


class CourseListView(GenericAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request) -> Response:
        """Returns list of courses"""
        result = CourseSelector.all()
        return Response(self.get_serializer(result, many=True).data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Creates course"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        course = container().course_service.create_course(request.user, serializer.validated_data["name"])
        return Response(self.get_serializer(course).data, status=status.HTTP_201_CREATED)


class CourseDetailsView(GenericAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request, course_id: UUID) -> Response:
        """Returns single course details"""
        result = CourseSelector.get_by_id(course_id)
        return Response(self.get_serializer(result).data, status=status.HTTP_200_OK)

    def put(self, request: Request, course_id: UUID) -> Response:
        """Updates single course details"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        course = container().course_service.update_course(request.user, course_id, **serializer.validated_data)
        return Response(self.get_serializer(course).data, status=status.HTTP_200_OK)

    def patch(self, request: Request, course_id: UUID) -> Response:
        """Partially updates single course details"""
        serializer = self.get_serializer(data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        course = container().course_service.update_course(request.user, course_id, **serializer.validated_data)
        return Response(self.get_serializer(course).data, status=status.HTTP_200_OK)

    def delete(self, request: Request, course_id: UUID) -> Response:
        """Deletes course"""
        container().course_service.delete_course(request.user, course_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseGroupsView(GenericAPIView):
    serializer_class = CourseGroupRelationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, course_id: UUID, group_id: int) -> Response:
        """Adds/updates single course group relation"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        container().course_service.course_add_group(request.user, course_id, group_id, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request, course_id: UUID, group_id: int) -> Response:
        """Deletes course group relation"""
        container().course_service.course_delete_group(request.user, course_id, group_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseLecturersView(GenericAPIView):
    serializer_class = CourseLecturerRelationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, course_id: UUID, lecturer_id: UUID) -> Response:
        """Adds/updates single course lecturer relation"""
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        container().course_service.course_add_lecturer(
            request.user, course_id, lecturer_id, **serializer.validated_data
        )
        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request, course_id: UUID, lecturer_id: UUID) -> Response:
        """Deletes course lecturer relation"""
        container().course_service.course_delete_lecturer(request.user, course_id, lecturer_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
