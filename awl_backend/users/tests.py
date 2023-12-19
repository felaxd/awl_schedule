from django.test import TestCase, Client
from django.urls import reverse

from users.models import Group
from users.serializers import GroupSerializer


class TestGroupListViewGet(TestCase):
    def setUp(self):
        self.endpoint = reverse("group-list")
        self.client = Client()

    def test_all_published_groups_will_be_returned(self):
        group1 = Group.objects.create(name="Group1", is_public=True)
        group2 = Group.objects.create(name="Group2", is_public=True)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn(GroupSerializer(group1).data, response.data)
        self.assertIn(GroupSerializer(group2).data, response.data)

    def test_not_published_groups_will_be_filtered(self):
        group1 = Group.objects.create(name="Group1", is_public=True)
        group2 = Group.objects.create(name="Group2", is_public=False)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn(GroupSerializer(group1).data, response.data)
        self.assertNotIn(GroupSerializer(group2).data, response.data)
