from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy


class MicroblogRssFeedTests(TestCase):
    url_name = 'tests:microblog-feed'

    def setUp(self):
        self.content = 'this is a microblog post'
        mommy.make('tests.MicroBlogPost', content=self.content)
        self.view_url = reverse(self.url_name)

    def test_get(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_get_has_content(self):
        response = self.client.get(self.view_url)
        # a very simple test to check if the content is in the response
        self.assertIn(self.content, response.content.decode('utf-8'))
