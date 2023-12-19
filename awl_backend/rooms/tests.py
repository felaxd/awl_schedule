from django.test import TestCase, Client
from django.urls import reverse

from rooms.models import Room
from rooms.serializers import RoomSerializer


class TestRoomListViewGet(TestCase):
    def setUp(self):
        self.endpoint = reverse("room-list")
        self.client = Client()

    def test_all_published_rooms_will_be_returned(self):
        room1 = Room.objects.create(name="Room1", is_public=True)
        room2 = Room.objects.create(name="Room2", is_public=True)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(RoomSerializer(room1).data, response.data)
        self.assertIn(RoomSerializer(room2).data, response.data)

    def test_not_published_rooms_will_be_filtered(self):
        room1 = Room.objects.create(name="Room1", is_public=True)
        room2 = Room.objects.create(name="Room2", is_public=False)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(RoomSerializer(room1).data, response.data)
        self.assertNotIn(RoomSerializer(room2).data, response.data)
