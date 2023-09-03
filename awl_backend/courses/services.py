from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.db import transaction

from common.utils import django_log_action
from common.validators import validate_user_permission
from courses.models import Course, GroupCourseThrough, LecturerCourseThrough
from courses.selectors import CourseSelector
from lecturers.selectors import LecturerSelector
from users.models import User, Group
from users.selectors import GroupSelector


@dataclass
class CourseService:
    @staticmethod
    @transaction.atomic()
    def create_course(user: User, name: str) -> Course:
        course = Course(name=name)
        validate_user_permission(user, course.ADD_PERMISSION_CODENAME, raise_error=True)
        course.full_clean()
        course.save()

        django_log_action(user=user, obj=course, action_flag=ADDITION)
        return course

    @staticmethod
    @transaction.atomic()
    def update_course(user: User, course_id: UUID, name: str) -> Course:
        course = CourseSelector.get_by_id(course_id)
        validate_user_permission(user, course.CHANGE_PERMISSION_CODENAME, raise_error=True)

        Course.objects.filter(id=course.id).update(name=name)
        course.refresh_from_db()
        course.full_clean()

        changed = course.changed_fields
        if changed:
            change_message = [{"changed": {"fields": changed}}]
            django_log_action(user=user, obj=course, action_flag=CHANGE, change_message=change_message)
        return course

    @staticmethod
    @transaction.atomic()
    def delete_course(user: User, course_id: UUID) -> None:
        course = CourseSelector.get_by_id(course_id)
        validate_user_permission(user, course.DELETE_PERMISSION_CODENAME, raise_error=True)
        course.delete()

        django_log_action(user=user, obj=course, action_flag=DELETION)
        return None

    @staticmethod
    @transaction.atomic()
    def course_add_group(user: User, course_id: UUID, group_id: int, **kwargs: Any) -> Course:
        course = CourseSelector.get_by_id(course_id)
        group = GroupSelector.get_by_id(group_id)
        validate_user_permission(user, course.CHANGE_PERMISSION_CODENAME, raise_error=True)
        validate_user_permission(user, group.CHANGE_PERMISSION_CODENAME, raise_error=True)

        model_fields = [field.name for field in GroupCourseThrough._meta.fields]
        kwargs = {k: kwargs[k] for k in model_fields if k in kwargs.keys()}

        GroupCourseThrough.objects.update_or_create(course=course, group=group, defaults=kwargs)

        change_message = [{"changed": {"fields": ["groups"]}}]
        django_log_action(user=user, obj=course, action_flag=CHANGE, change_message=change_message)
        return course

    @staticmethod
    @transaction.atomic()
    def course_delete_group(user: User, course_id: UUID, group_id: int) -> Course:
        course = CourseSelector.get_by_id(course_id)
        group = GroupSelector.get_by_id(group_id)
        validate_user_permission(user, course.CHANGE_PERMISSION_CODENAME, raise_error=True)
        validate_user_permission(user, group.CHANGE_PERMISSION_CODENAME, raise_error=True)

        course.groups.remove(group)

        change_message = [{"changed": {"fields": ["groups"]}}]
        django_log_action(user=user, obj=course, action_flag=CHANGE, change_message=change_message)
        return course

    @staticmethod
    @transaction.atomic()
    def course_add_lecturer(user: User, course_id: UUID, lecturer_id: UUID, group: Group, **kwargs: Any) -> Course:
        course = CourseSelector.get_by_id(course_id)
        lecturer = LecturerSelector.get_by_id(lecturer_id)
        validate_user_permission(user, course.CHANGE_PERMISSION_CODENAME, raise_error=True)
        validate_user_permission(user, lecturer.CHANGE_PERMISSION_CODENAME, raise_error=True)
        validate_user_permission(user, group.CHANGE_PERMISSION_CODENAME, raise_error=True)

        model_fields = [field.name for field in LecturerCourseThrough._meta.fields]
        kwargs = {k: kwargs[k] for k in model_fields if k in kwargs.keys()}

        LecturerCourseThrough.objects.update_or_create(course=course, lecturer=lecturer, group=group, defaults=kwargs)

        change_message = [{"changed": {"fields": ["lecturers"]}}]
        django_log_action(user=user, obj=course, action_flag=CHANGE, change_message=change_message)
        return course

    @staticmethod
    @transaction.atomic()
    def course_delete_lecturer(user: User, course_id: UUID, lecturer_id: UUID) -> Course:
        course = CourseSelector.get_by_id(course_id)
        lecturer = LecturerSelector.get_by_id(lecturer_id)
        validate_user_permission(user, course.CHANGE_PERMISSION_CODENAME, raise_error=True)
        validate_user_permission(user, lecturer.CHANGE_PERMISSION_CODENAME, raise_error=True)

        course.lecturers.remove(lecturer)

        change_message = [{"changed": {"fields": ["lecturers"]}}]
        django_log_action(user=user, obj=course, action_flag=CHANGE, change_message=change_message)
        return course
