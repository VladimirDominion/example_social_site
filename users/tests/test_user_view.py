from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.tests.base_api_test import BaseAPITestCase


class TestUserView(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_email = 'test2@example.com'
        cls.user_password = '1qaz2ws3e4'
        cls.user = cls.create_user(email=cls.user_email, password=cls.user_password)

    def test_sign_up_success(self):
        url = reverse('user-sign-up')
        data = dict(email='test@example.com', password='1qaz2ws3e4', password_repeat='1qaz2ws3e4')
        res = self.client.post(url, data=data,  format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        json_data = res.json()
        self.assertEqual('test@example.com', json_data['email'])

    def test_sign_up_wrong_repeat_password(self):
        url = reverse('user-sign-up')
        data = dict(email='test@example.com', password='1qaz2ws3e4', password_repeat='1qaz2w')
        res = self.client.post(url, data=data,  format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_user_which_already_exist(self):
        url = reverse('user-sign-up')
        data = dict(email=self.user_email, password='1qaz2ws3e4', password_repeat='1qaz2ws3e4')
        res = self.client.post(url, data=data,  format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        url = reverse('user-login')
        data = dict(email=self.user_email, password=self.user_password)
        res = self.client.post(url, data=data,  format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        json_data = res.json()
        self.assertEqual(self.user_email, json_data['email'])

    def test_login_wrong_email(self):
        url = reverse('user-login')
        data = dict(email='sasdasd', password=self.user_password)
        res = self.client.post(url, data=data,  format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_me_success(self):
        url = reverse('user-me')
        token = self.get_jwt_token(email=self.user_email, password=self.user_password)
        res = self.make_authenticated_request(url=url, method='get', jwt_token=token)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        json_data = res.json()
        self.assertEqual(self.user_email, json_data['email'])

    def test_change_password_success(self):
        url = reverse('user-change-password')
        data = dict(old_password=self.user_password, new_password='1qaz2ws3e4567', new_password_repeat='1qaz2ws3e4567')
        token = self.get_jwt_token(email=self.user_email, password=self.user_password)
        res = self.make_authenticated_request(url=url, method='post', jwt_token=token, **data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_change_password_week_new_password(self):
        url = reverse('user-change-password')
        data = dict(old_password=self.user_password, new_password='1123', new_password_repeat='1123')
        token = self.get_jwt_token(email=self.user_email, password=self.user_password)
        res = self.make_authenticated_request(url=url, method='post', jwt_token=token, **data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_new_password_mismatch(self):
        url = reverse('user-change-password')
        data = dict(old_password=self.user_password, new_password='1qaz2ws3e34r5', new_password_repeat='sdfsdfsdfsdfsdf')
        token = self.get_jwt_token(email=self.user_email, password=self.user_password)
        res = self.make_authenticated_request(url=url, method='post', jwt_token=token, **data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

