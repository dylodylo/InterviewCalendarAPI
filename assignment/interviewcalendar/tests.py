from django.test import TestCase
from .models import User
import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class UserModelTest(TestCase):
    """
    Test module for User model
    """

    def setUp(self) -> None:
        self.testuser1 = User.objects.create_user(username='TestUser1', password='password', slots={"slots":["20/06/2021 12:00-13:00", "20/06/2021 13:00-14:00"]})
        self.testuser2 = User.objects.create_user(username='TestUser2', password='password', slots={"slots":["20/06/2021 12:00-13:00", "20/06/2021 14:00-15:00"]})
        self.testuser3 = User.objects.create_user(username='TestUser3', password='password', slots={"slots":["20/06/2021 12:00-13:00", "20/06/2021 15:00-16:00"]})
        self.valid_slots = {"slots":["20/06/2021 11:00-12:00"]}
        self.valid_added_slots = {**self.testuser1.slots, **self.valid_slots}
        self.client = APIClient()
        self.valid_slotes_returned = ["20/06/2021 12:00-13:00"]

    def test_user_creation(self):
        users_count = len(User.objects.all())
        self.assertEqual(users_count, 3)

    def test_valid_patch(self):
        self.client.login(username=self.testuser1.username, password='password')
        response = self.client.patch(reverse('slots_update', args=(self.testuser1.id,)), data=json.dumps({"slots": self.valid_slots}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_patch_user_slots(self):
        self.client.login(username=self.testuser1.username, password='password')
        response = self.client.patch(reverse('slots_update', args=(self.testuser1.id,)), data=json.dumps({"slots": self.valid_slots}), content_type='application/json')
        self.testuser1.refresh_from_db()
        self.assertEqual(self.valid_added_slots['slots'].sort(), self.testuser1.slots['slots'].sort())
        self.client.logout()

    def test_invalid_value_patch(self):
        self.client.login(username=self.testuser1.username, password='password')
        url = reverse('slots_update', args=(self.testuser1.id,))
        invalid_value = ["20/06/2021 11:00-12:00"]
        response = self.client.patch(url, data=json.dumps({"slots": invalid_value}), content_type='application/json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_date_patch(self):
        self.client.login(username=self.testuser1.username, password='password')
        url = reverse('slots_update', args=(self.testuser1.id,))
        invalid_date = ["20/06/21 11:00-12:00"]
        response = self.client.patch(url, data=json.dumps({"slots": invalid_date}), content_type='application/json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_hours_patch(self):
        self.client.login(username=self.testuser1.username, password='password')
        url = reverse('slots_update', args=(self.testuser1.id,))
        invalid_hours = ["20/06/2021 11:30-12:00"]
        response = self.client.patch(url, data=json.dumps({"slots": invalid_hours}), content_type='application/json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_dates_list(self):
        response = self.client.get(reverse('get_slots', args=(self.testuser1.id,)), {"r_ids": "2,3"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_dates_list_return(self):
        response = self.client.get(reverse('get_slots', args=(self.testuser1.id,)), {"r_ids": "2,3"})
        data = response.json()
        self.assertEqual(data, self.valid_slotes_returned)

