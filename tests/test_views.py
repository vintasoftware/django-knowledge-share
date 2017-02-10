import json

from django.test import TestCase, override_settings
from django.test.client import Client
from django.core.urlresolvers import reverse

import responses

from tests.models import MicroBlogPost
from knowledge_share.views import (
    SlackSlashWebHookView,
    _normalize_and_split_data,
    _clean_category_name,
)


@override_settings(
    SLACK_TOKEN='1234',
)
class SlackSlashWebHookViewTests(TestCase):

    url_name = 'tests:microblog-slack-slash'
    view = SlackSlashWebHookView

    def setUp(self):
        self.view_url = reverse(self.url_name)
        self.client = Client(HTTP_HOST='localtest.com')
        self.post_params = {
            'text': '[My blog Post][category]',
            'token': '1234',
        }

    def test_post_with_invalid_params(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 400)

    def test_post_with_invalid_token_params(self):
        self.post_params['token'] = '123'
        response = self.client.post(self.view_url, self.post_params)
        self.assertEqual(response.status_code, 400)

    @responses.activate
    def test_post_with_valid_params(self):
        responses.add(
            responses.POST,
            'https://api.twitter.com/1.1/statuses/update.json',
            body='{"success": "created"}', status=200,
            content_type='application/json'
        )
        response = self.client.post(self.view_url, self.post_params)
        self.assertEqual(response.status_code, 200)

    @override_settings(KNOWLEDGE_USE_TWITTER=False)
    def test_post_without_categories(self):
        self.post_params['text'] = '[My blog Post]'
        response = self.client.post(self.view_url, self.post_params)
        self.assertEqual(response.status_code, 200)
        microblog_post = MicroBlogPost.objects.first()
        self.assertEqual(microblog_post.content, 'My blog Post')
        self.assertEqual(microblog_post.category.count(), 0)

    @responses.activate
    def test_post_with_valid_params_create_an_object(self):
        responses.add(
            responses.POST,
            'https://api.twitter.com/1.1/statuses/update.json',
            body='{"success": "created"}', status=200,
            content_type='application/json'
        )
        self.client.post(self.view_url, self.post_params)
        microblog_post = MicroBlogPost.objects.first()
        self.assertEqual(microblog_post.content, 'My blog Post')

    @responses.activate
    def test_post_with_valid_params_post_on_twitter(self):
        responses.add(
            responses.POST,
            'https://api.twitter.com/1.1/statuses/update.json',
            body='{"success": "created"}', status=200,
            content_type='application/json'
        )
        self.client.post(self.view_url, self.post_params)
        microblog_post = MicroBlogPost.objects.first()
        self.assertTrue(microblog_post.posted_on_twitter)

    @responses.activate
    def test_post_create_category_tags(self):
        responses.add(
            responses.POST,
            'https://api.twitter.com/1.1/statuses/update.json',
            body='{"success": "created"}', status=200,
            content_type='application/json'
        )
        self.client.post(self.view_url, self.post_params)
        microblog_post = MicroBlogPost.objects.first()
        category = microblog_post.category.first()
        self.assertTrue(category.name, 'category')

    @responses.activate
    def test_post_with_twitter_error(self):
        responses.add(
            responses.POST,
            'https://api.twitter.com/1.1/statuses/update.json',
            body='{"success": "created"}', status=400,
            content_type='application/json'
        )
        response = self.client.post(self.view_url, self.post_params)
        self.assertIn('(it worked! But twitter posting failed)',
                      json.loads(response.content)['text'])


class SlackSlashCommandHelpersTest(TestCase):

    def test_normalize_and_split_data(self):
        content = _normalize_and_split_data('[My blog Post][category]')
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], 'My blog Post')
        self.assertEqual(content[1], 'category')

    def test_normalize_without_category(self):
        content = _normalize_and_split_data('[My blog Post]')
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], 'My blog Post')
        self.assertEqual(content[1], '')

    def test_clean_category_name(self):
        category = _clean_category_name(' Category')
        self.assertEqual(category, 'category')
