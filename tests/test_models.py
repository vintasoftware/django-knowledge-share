from django.test import TestCase

from knowledge_share.conf import KNOWLEDGE_APP_NAME
from model_mommy import mommy


class MicroBlogCategoryTest(TestCase):
    def test_format_hashtag_category(self):
        category = mommy.make(
            KNOWLEDGE_APP_NAME + '.MicroBlogCategory',
            name='chrome'
        )
        self.assertEqual(category.hashtag, '#Chrome')

    def test_format_hashtag_category_with_space(self):
        category = mommy.make(
            KNOWLEDGE_APP_NAME + '.MicroBlogCategory',
            name='chrome extension'
        )
        self.assertEqual(category.hashtag, '#ChromeExtension')

    def test_str(self):
        category = mommy.make(KNOWLEDGE_APP_NAME + '.MicroBlogCategory')
        self.assertEquals(str(category), category.name)


class MicroBlogPostTest(TestCase):

    def test_remove_http_url_from_content(self):
        text = (
            'This is the http post text http://some.url.com more text'
            'with more text This is the post'
        )
        microblog_post = mommy.make(KNOWLEDGE_APP_NAME + '.MicroBlogPost', content=text)
        text_response = (
            'This is the http post text more text'
            'with more text This is the post'
        )
        self.assertEqual(microblog_post._remove_url_from_content(), text_response)

    def test_remove_https_url_from_content(self):
        text = (
            'This is the https post text http://some.url.com more text'
            'with more text This is the post'
        )
        microblog_post = mommy.make(KNOWLEDGE_APP_NAME + '.MicroBlogPost', content=text)
        text_response = (
            'This is the https post text more text'
            'with more text This is the post'
        )
        self.assertEqual(microblog_post._remove_url_from_content(), text_response)

    def test_content_to_slug(self):
        text = (
            'This is the post text '
            'with more text This is the post'
        )
        microblog_post = mommy.make(KNOWLEDGE_APP_NAME + '.MicroBlogPost', content=text)
        slug = microblog_post._content_to_slug()
        self.assertEqual(slug, 'This-is-the-post-text-with')
