import responses

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from tests.models import MicroBlogPost
from vinta_microblog.views import (
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


class SlackSlashCommandHelpersTest(TestCase):

    def test_normalize_and_split_data(self):
        content = _normalize_and_split_data('[My blog Post][category]')
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], 'My blog Post')
        self.assertEqual(content[1], 'category')

    def test_clean_category_name(self):
        category = _clean_category_name(' Category')
        self.assertEqual(category, 'category')
