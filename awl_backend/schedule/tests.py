from datetime import timedelta

import freezegun
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from lecturers.models import Lecturer
from rooms.models import Room
from schedule.models import ScheduleBlock
from schedule.serializers import ScheduleBlockSerializer
from users.models import Group


class TestScheduleBlockListViewGet(TestCase):
    def setUp(self):
        self.endpoint = reverse("schedule-block-list")
        self.client = Client()

    def test_all_published_schedule_blocks_will_be_returned(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(course_name="Course1", start=start, end=end, is_public=True)
        schedule_block2 = ScheduleBlock.objects.create(course_name="Course2", start=start, end=end, is_public=True)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    def test_not_published_schedule_blocks_will_be_filtered(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(course_name="Course1", start=start, end=end, is_public=True)
        schedule_block2 = ScheduleBlock.objects.create(course_name="Course2", start=start, end=end, is_public=False)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertNotIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    @freezegun.freeze_time()
    def test_schedule_blocks_can_be_filtered_by_date_from(self):
        """
        In this case sb1 is in two days from now, so should be returned as we ask for blocks after tomorrow
        Sb2 was finished yesterday so should not be returned
        """
        schedule_block1_start = timezone.now() + timedelta(days=2)
        schedule_block1_end = schedule_block1_start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(
            course_name="Course1", start=schedule_block1_start, end=schedule_block1_end, is_public=True
        )

        schedule_block2_start = timezone.now() - timedelta(days=1)
        schedule_block2_end = schedule_block2_start + timedelta(hours=1)
        schedule_block2 = ScheduleBlock.objects.create(
            course_name="Course2", start=schedule_block2_start, end=schedule_block2_end, is_public=True
        )

        tomorrow = (timezone.now() + timedelta(days=1)).date()
        response = self.client.get(self.endpoint + f"?date_from={tomorrow.isoformat()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertNotIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    @freezegun.freeze_time()
    def test_schedule_blocks_can_be_filtered_by_date_to(self):
        """
        In this case sb1 is in two days from now, so should not be returned as we ask for blocks up to tomorrow
        Sb2 was finished yesterday so should be returned
        """
        schedule_block1_start = timezone.now() + timedelta(days=2)
        schedule_block1_end = schedule_block1_start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(
            course_name="Course1", start=schedule_block1_start, end=schedule_block1_end, is_public=True
        )

        schedule_block2_start = timezone.now() - timedelta(days=1)
        schedule_block2_end = schedule_block2_start + timedelta(hours=1)
        schedule_block2 = ScheduleBlock.objects.create(
            course_name="Course2", start=schedule_block2_start, end=schedule_block2_end, is_public=True
        )

        tomorrow = (timezone.now() + timedelta(days=1)).date()
        response = self.client.get(self.endpoint + f"?date_to={tomorrow.isoformat()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertNotIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    @freezegun.freeze_time()
    def test_schedule_blocks_can_be_filtered_by_timerange(self):
        """In this case sb1 and sb2 are in date range. Sb3 is a week after timerange so should be filtered out"""
        schedule_block1_start = timezone.now() + timedelta(days=2)
        schedule_block1_end = schedule_block1_start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(
            course_name="Course1", start=schedule_block1_start, end=schedule_block1_end, is_public=True
        )

        schedule_block2_start = timezone.now() - timedelta(days=1)
        schedule_block2_end = schedule_block2_start + timedelta(hours=1)
        schedule_block2 = ScheduleBlock.objects.create(
            course_name="Course2", start=schedule_block2_start, end=schedule_block2_end, is_public=True
        )

        schedule_block3_start = timezone.now() - timedelta(weeks=2)
        schedule_block3_end = schedule_block2_start + timedelta(hours=1)
        schedule_block3 = ScheduleBlock.objects.create(
            course_name="Course2", start=schedule_block3_start, end=schedule_block3_end, is_public=True
        )

        week_start = (timezone.now() - timedelta(weeks=1)).date()
        week_end = (timezone.now() + timedelta(weeks=1)).date()
        response = self.client.get(
            self.endpoint + f"?date_from={week_start.isoformat()}&date_to={week_end.isoformat()}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertIn(ScheduleBlockSerializer(schedule_block2).data, response.data)
        self.assertNotIn(ScheduleBlockSerializer(schedule_block3).data, response.data)

    def test_schedule_blocks_can_be_filtered_by_lecturer(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(course_name="Course1", start=start, end=end, is_public=True)
        schedule_block2 = ScheduleBlock.objects.create(course_name="Course2", start=start, end=end, is_public=True)

        lecturer = Lecturer.objects.create(first_name="Lecturer", last_name="1", is_public=True)
        schedule_block1.lecturers.add(lecturer, through_defaults={"room": None})

        response = self.client.get(self.endpoint + f"?lecturers={lecturer.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertNotIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    def test_schedule_blocks_can_be_filtered_by_multiple_lecturers(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(course_name="Course1", start=start, end=end, is_public=True)
        schedule_block2 = ScheduleBlock.objects.create(course_name="Course2", start=start, end=end, is_public=True)

        lecturer1 = Lecturer.objects.create(first_name="Lecturer", last_name="1", is_public=True)
        schedule_block1.lecturers.add(lecturer1, through_defaults={"room": None})

        lecturer2 = Lecturer.objects.create(first_name="Lecturer", last_name="2", is_public=True)
        schedule_block2.lecturers.add(lecturer1, through_defaults={"room": None})

        response = self.client.get(self.endpoint + f"?lecturers={lecturer1.id}&lecturers={lecturer2.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    def test_schedule_blocks_can_be_filtered_by_room(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(course_name="Course1", start=start, end=end, is_public=True)
        schedule_block2 = ScheduleBlock.objects.create(course_name="Course2", start=start, end=end, is_public=True)

        room = Room.objects.create(name="Room1", is_public=True)
        schedule_block1.rooms.add(room)

        response = self.client.get(self.endpoint + f"?rooms={room.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertNotIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    def test_schedule_blocks_can_be_filtered_by_multiple_rooms(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(course_name="Course1", start=start, end=end, is_public=True)
        schedule_block2 = ScheduleBlock.objects.create(course_name="Course2", start=start, end=end, is_public=True)

        room1 = Room.objects.create(name="Room1", is_public=True)
        schedule_block1.rooms.add(room1)

        room2 = Room.objects.create(name="Room2", is_public=True)
        schedule_block2.rooms.add(room2)

        response = self.client.get(self.endpoint + f"?rooms={room1.id}&rooms={room2.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    def test_schedule_blocks_can_be_filtered_by_group(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(course_name="Course1", start=start, end=end, is_public=True)
        schedule_block2 = ScheduleBlock.objects.create(course_name="Course2", start=start, end=end, is_public=True)

        group = Group.objects.create(name="Group1", is_public=True)
        schedule_block1.groups.add(group)

        response = self.client.get(self.endpoint + f"?groups={group.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertNotIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    def test_schedule_blocks_can_be_filtered_by_multiple_groups(self):
        start = timezone.now()
        end = start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(course_name="Course1", start=start, end=end, is_public=True)
        schedule_block2 = ScheduleBlock.objects.create(course_name="Course2", start=start, end=end, is_public=True)

        group1 = Group.objects.create(name="Group1", is_public=True)
        schedule_block1.groups.add(group1)

        group2 = Group.objects.create(name="Group2", is_public=True)
        schedule_block2.groups.add(group2)

        response = self.client.get(self.endpoint + f"?groups={group1.id}&groups={group2.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    def test_schedule_blocks_can_be_filtered_by_mix_of_parameters_case1(self):
        """
        Filter by room and group
        Sb1 has correct group and room
        Sb2 has only correct room
        """
        start = timezone.now()
        end = start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(course_name="Course1", start=start, end=end, is_public=True)
        schedule_block2 = ScheduleBlock.objects.create(course_name="Course2", start=start, end=end, is_public=True)

        group = Group.objects.create(name="Group1", is_public=True)
        schedule_block1.groups.add(group)

        room = Room.objects.create(name="Room1", is_public=True)
        schedule_block1.rooms.add(room)
        schedule_block2.rooms.add(room)

        response = self.client.get(self.endpoint + f"?groups={group.id}&rooms={room.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertNotIn(ScheduleBlockSerializer(schedule_block2).data, response.data)

    def test_schedule_blocks_can_be_filtered_by_mix_of_parameters_case2(self):
        """
        Filter by group and timerange
        Sb1 has correct group and is in timerange
        Sb2 is in correct timerange, but has no requested group
        Sb3 has correct group but is not in timerange
        """
        schedule_block1_start = timezone.now() + timedelta(days=2)
        schedule_block1_end = schedule_block1_start + timedelta(hours=1)
        schedule_block1 = ScheduleBlock.objects.create(
            course_name="Course1", start=schedule_block1_start, end=schedule_block1_end, is_public=True
        )

        schedule_block2_start = timezone.now() - timedelta(days=1)
        schedule_block2_end = schedule_block2_start + timedelta(hours=1)
        schedule_block2 = ScheduleBlock.objects.create(
            course_name="Course2", start=schedule_block2_start, end=schedule_block2_end, is_public=True
        )

        schedule_block3_start = timezone.now() - timedelta(weeks=2)
        schedule_block3_end = schedule_block2_start + timedelta(hours=1)
        schedule_block3 = ScheduleBlock.objects.create(
            course_name="Course2", start=schedule_block3_start, end=schedule_block3_end, is_public=True
        )

        group = Group.objects.create(name="Group1", is_public=True)
        schedule_block1.groups.add(group)
        schedule_block3.groups.add(group)

        week_start = (timezone.now() - timedelta(weeks=1)).date()
        week_end = (timezone.now() + timedelta(weeks=1)).date()
        response = self.client.get(
            self.endpoint + f"?groups={group.id}&date_from={week_start.isoformat()}&date_to={week_end.isoformat()}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(ScheduleBlockSerializer(schedule_block1).data, response.data)
        self.assertNotIn(ScheduleBlockSerializer(schedule_block2).data, response.data)
        self.assertNotIn(ScheduleBlockSerializer(schedule_block3).data, response.data)
