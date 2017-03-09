import json

from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.test.client import Client
from tests.models import MicroBlogPost

import mock
import responses
from knowledge_share.views import (_clean_category_name,
                                   _normalize_and_split_data)


@override_settings(
    SLACK_TOKEN='1234',
)
class SlackSlashWebHookViewTests(TestCase):
    url_name = 'tests:microblog-slack-slash'

    def setUp(self):
        self.view_url = reverse(self.url_name)
        self.client = Client(HTTP_HOST='localtest.com')
        self.post_params = {
            'text': 'My blog Post [category]',
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
        self.post_params['text'] = 'My blog Post'
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

    @mock.patch('knowledge_share.twitter_helpers.logger')
    @responses.activate
    def test_post_with_twitter_error(self, mocked):
        responses.add(
            responses.POST,
            'https://api.twitter.com/1.1/statuses/update.json',
            body='{"success": "created"}', status=400,
            content_type='application/json'
        )
        response = self.client.post(self.view_url, self.post_params)
        mocked.error.assert_called_once_with(
            "Tried to post a microblog post on Twitter but got a ClientError,"
            " check your twitter keys.")
        self.assertIn('(it worked! But twitter posting failed)',
                      json.loads(response.content.decode('utf-8'))['text'])


class SlackSlashCommandHelpersTest(TestCase):

    def test_normalize_and_split_data(self):
        content = _normalize_and_split_data('My blog Post[category]')
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], 'My blog Post')
        self.assertEqual(content[1], 'category')

    def test_normalize_and_split_data_with_square_braces(self):
        content = _normalize_and_split_data('A list is like this foo[1], awesome.')
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], 'A list is like this foo[1], awesome.')
        self.assertEqual(content[1], '')

    def test_normalize_and_split_data_with_square_braces_and_category(self):
        content = _normalize_and_split_data(
            'A list is like this foo[1][Python]')
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], 'A list is like this foo[1]')
        self.assertEqual(content[1], 'Python')

    def test_normalize_and_split_data_with_square_braces_and_space_category(self):
        content = _normalize_and_split_data(
            'A list is like this foo[1] [Python]')
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], 'A list is like this foo[1]')
        self.assertEqual(content[1], 'Python')

    def test_normalize_and_split_data_with_multiple_categories(self):
        content = _normalize_and_split_data('My blog Post[Python, Django]')
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], 'My blog Post')
        self.assertEqual(content[1], 'Python, Django')

    def test_normalize_without_category(self):
        content = _normalize_and_split_data('My blog Post')
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], 'My blog Post')
        self.assertEqual(content[1], '')

    def test_clean_category_name(self):
        category = _clean_category_name(' Category')
        self.assertEqual(category, 'category')
