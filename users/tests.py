from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.tests.base_api_test import BaseAPITestCase


class TestUserView(BaseAPITestCase):
    def test_sign_up_success(self):
        url = reverse('user-sign-up')
        data = dict(email='test@example.com', password='1qaz2ws3e4', password_repeat='1qaz2ws3e4')
        res = self.client.post(url, data=data,  format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        json_data = res.json()
        self.assertEqual('test@example.com', json_data['email'])

