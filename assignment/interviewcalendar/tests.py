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
        self.testuser1 = User.objects.create_user(username='TestUser1', password='password', slots={"20-06-2021": [ 4, 5, 6 ]})
        self.testuser2 = User.objects.create_user(username='TestUser2', password='password', slots={"20-06-2021": [ 6, 7, 8 ]})
        self.testuser3 = User.objects.create_user(username='TestUser3', password='password', slots={"20-06-2021": [ 1, 6, 8 ]})
        self.valid_slots = {"22-06-2021": [ 1, 2, 3 ]}
        self.valid_added_slots = {**self.testuser1.slots, **self.valid_slots} #combine two dicts
        self.client = APIClient()
        self.valid_slotes_returned = {"20-06-2021": [ 6 ]}

    def test_user_creation(self):
        users_count = len(User.objects.all())
        self.assertEqual(users_count, 3)

    def test_valid_patch(self):
        self.client.login(username=self.testuser1.username, password='password')
        response = self.client.patch(f'/users/{self.testuser1.id}', data=json.dumps({"slots": self.valid_slots}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_patch_user_slots(self):
        self.client.login(username=self.testuser1.username, password='password')
        response = self.client.patch(f'/users/{self.testuser1.id}', data=json.dumps({"slots": self.valid_slots}), content_type='application/json')
        self.testuser1.refresh_from_db()
        self.assertEqual(self.valid_added_slots, self.testuser1.slots)
        self.client.logout()

    def test_invalid_key_patch(self):
        self.client.login(username=self.testuser1.username, password='password')
        url = f'/users/{self.testuser1.id}'
        invalid_key = {"20-20-20": [ 1, 6, 7 ]}
        response = self.client.patch(url, data=json.dumps({"slots": invalid_key}), content_type='application/json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_value_patch(self):
        self.client.login(username=self.testuser1.username, password='password')
        url = f'/users/{self.testuser1.id}'
        invalid_value = {"20-02-2022": "hours"}
        response = self.client.patch(url, data=json.dumps({"slots": invalid_value}), content_type='application/json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_date_patch(self):
        self.client.login(username=self.testuser1.username, password='password')
        url = f'/users/{self.testuser1.id}'
        invalid_date = {"20-02-2019": [ 1, 6, 7 ]}
        response = self.client.patch(url, data=json.dumps({"slots": invalid_date}), content_type='application/json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_hours_patch(self):
        self.client.login(username=self.testuser1.username, password='password')
        url = f'/users/{self.testuser1.id}'
        invalid_hours = {"20-02-2022": [ -1, 6, 7 ]}
        response = self.client.patch(url, data=json.dumps({"slots": invalid_hours}), content_type='application/json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_dates_list(self):
        response = self.client.get(f'/users/{self.testuser1.id}/dates/', {"r_ids": "2,3"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_dates_list_return(self):
        response = self.client.get(f'/users/{self.testuser1.id}/dates/', {"r_ids": "2,3"})
        data = response.json()
        self.assertEqual(data, self.valid_slotes_returned)

