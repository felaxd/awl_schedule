from typing import cast, Type

from dependencies import Injector

from courses.services import CourseService
from lecturers.services import LecturerService
from rooms.services import RoomService
from schedule.services import ScheduleBlockService, ExcelScheduleService, ScheduleService
from users.services import UserService, GroupService


class Container(Injector):
    """
    Injects all the needed dependencies to the service.
    Every service created should be casted here, so it won't be missed in the future development.

    Container is like huge family, every child knows all the other children.
    Let's say that Service (child) 'A' throws a party that he needs Service (other child) 'B' to be present.
    Service 'B' needs Service C to be present also, and so on, and so on.
    In that case while implementing Service 'A' we have to remember all the relations between services.
    Container comes to the rescue - it knows all the children, so we just need to invite him to the party.
    All the required Services will come with him.
    (of course there is a lot of background logic here, but im sure that you get the point of container now)

    Usage:
        container().service.method()
    Declaration:
        service = cast(Service, Service)
    """

    user_service = cast(UserService, UserService)
    group_service = cast(GroupService, GroupService)
    lecturer_service = cast(LecturerService, LecturerService)
    course_service = cast(CourseService, CourseService)
    room_service = cast(RoomService, RoomService)
    schedule_service = cast(ScheduleService, ScheduleService)
    schedule_block_service = cast(ScheduleBlockService, ScheduleBlockService)
    excel_schedule_service = cast(ExcelScheduleService, ExcelScheduleService)


def container() -> Type[Container]:
    return Container
