from django.test import TestCase, Client
from django.urls import reverse

from lecturers.models import Lecturer
from lecturers.serializers import LecturerSerializer


class TestLecturerListViewGet(TestCase):
    def setUp(self):
        self.endpoint = reverse("lecturer-list")
        self.client = Client()

    def test_all_published_lecturers_will_be_returned(self):
        lecturer1 = Lecturer.objects.create(first_name="Lecturer", last_name="1", is_public=True)
        lecturer2 = Lecturer.objects.create(first_name="Lecturer", last_name="2", is_public=True)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(LecturerSerializer(lecturer1).data, response.data)
        self.assertIn(LecturerSerializer(lecturer2).data, response.data)

    def test_not_published_lecturers_will_be_filtered(self):
        lecturer1 = Lecturer.objects.create(first_name="Lecturer", last_name="1", is_public=True)
        lecturer2 = Lecturer.objects.create(first_name="Lecturer", last_name="2", is_public=False)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(LecturerSerializer(lecturer1).data, response.data)
        self.assertNotIn(LecturerSerializer(lecturer2).data, response.data)
