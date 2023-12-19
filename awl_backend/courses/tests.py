from django.test import TestCase, Client
from django.urls import reverse

from courses.models import Course
from courses.serializers import CourseSerializer


class TestCourseListViewGet(TestCase):
    def setUp(self):
        self.endpoint = reverse("course-list")
        self.client = Client()

    def test_all_published_courses_will_be_returned(self):
        course1 = Course.objects.create(name="Course1", is_public=True)
        course2 = Course.objects.create(name="Course2", is_public=True)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(CourseSerializer(course1).data, response.data)
        self.assertIn(CourseSerializer(course2).data, response.data)

    def test_not_published_courses_will_be_filtered(self):
        course1 = Course.objects.create(name="Course1", is_public=True)
        course2 = Course.objects.create(name="Course2", is_public=False)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(CourseSerializer(course1).data, response.data)
        self.assertNotIn(CourseSerializer(course2).data, response.data)
