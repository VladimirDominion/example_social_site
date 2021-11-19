import json

from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient

from users.factories import UserFactory


class BaseAPITestCase(APITestCase):

    @classmethod
    def create_user(cls, email: str, password: str, **user_data):
        user = UserFactory(email=email, **user_data)
        user.set_password(password)
        user.save()
        return user

    def get_jwt_token(self, *, email, password):
        url = reverse('token_obtain_pair')
        res = self.client.post(url, {'email': email, 'password': password}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in res.data)
        token = res.data['access']
        return token

    @classmethod
    def make_authenticated_request(cls, *, url: str, method: str, jwt_token: str, **kwargs) -> Response:
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
        client_method = getattr(client, method)
        if kwargs:
            res = client_method(url, data=kwargs, format='json')
        else:
            res = client_method(url)
        return res

    def _test_auth_credentials(self, url, method):
        resp = getattr(self.client, method)(url)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json(), {'detail': 'Authentication credentials were not provided.'})