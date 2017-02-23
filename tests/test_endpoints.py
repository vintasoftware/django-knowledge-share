import json

from django.core.urlresolvers import reverse

from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from knowledge_share.conf import KNOWLEDGE_APP_NAME


class MicroblogPostRateUpdateAPIViewTests(APITestCase):
    url_name = 'tests:microblog-post-rate'

    def setUp(self):
        microblog_post = mommy.make(
            KNOWLEDGE_APP_NAME + '.MicroBlogPost',
            content='chrome extension'
        )
        self.view_url = reverse(self.url_name, kwargs={'pk': microblog_post.pk})

    def test_put_url_works(self):
        response = self.client.put(
            self.view_url,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_update_microblog_post_rate(self):
        response = self.client.put(
            self.view_url,
        )
        self.assertEqual(response.data['positive_rate'], 2)

    def test_put_set_cookie_with_id(self):
        response = self.client.put(
            self.view_url,
        )
        cookie = json.loads(response.cookies['posts_id'].value)
        self.assertEqual(cookie['posts_id'], [1])

    def test_put_set_cookie_with_previus_post_id(self):
        self.client.cookies['posts_id'] = "{\"posts_id\": [429]}"
        response = self.client.put(
            self.view_url,
        )
        cookie = json.loads(response.cookies['posts_id'].value)
        self.assertListEqual(cookie['posts_id'], [429, 1])
