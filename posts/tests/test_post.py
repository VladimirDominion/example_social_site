from django.urls import reverse
from rest_framework import status

from core.tests.base_api_test import BaseAPITestCase
from .factories import TagFactory


class TestPostViewSet(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_email = 'test2@example.com'
        cls.user_password = '1qaz2ws3e4'
        cls.user = cls.create_user(email=cls.user_email, password=cls.user_password)
        cls.tag1 = TagFactory()
        cls.tag2 = TagFactory()

    def test_post_create(self):
        post_data = {
            'title': 'test post',
            'text': 'test',
            'tags': [self.tag1.id, self.tag2.id]
        }
        url = reverse('post-list')
        token = self.get_jwt_token(email=self.user_email, password=self.user_password)
        res = self.make_authenticated_request(url=url, method='post', jwt_token=token, **post_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        json_data = res.json()
        self.assertEqual(post_data['title'], json_data['title'])
        self.assertEqual(post_data['text'], json_data['text'])
        self.assertEqual(len(json_data['tags']), 2)


