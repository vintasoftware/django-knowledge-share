from django.test import TestCase

from knowledge_share.conf import KNOWLEDGE_APP_NAME
from knowledge_share.twitter_helpers import (format_twitter_post,
                                             format_twitter_post_to_share)
from model_mommy import mommy


class FormatTwitterPostTests(TestCase):
    def test_post_format_to_post_directly(self):
        text = (
            'This is the post text http://some.url.com more text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
        )
        post = mommy.make(KNOWLEDGE_APP_NAME + '.MicroBlogPost', content=text, posted_on_twitter=True)
        formated = format_twitter_post(post)
        response = (
            'This is the post text http://some.url.com more text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text... '
            'http://www.vinta.com.br/lessons-learned/this-is-the-post-text-more/'
        )
        self.assertEqual(formated, response)

    def test_post_format_to_post_directly_with_category(self):
        text = (
            'This is the post text http://some.url.com more text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
        )

        category = mommy.make(KNOWLEDGE_APP_NAME + '.MicroBlogCategory', name="chrome")
        post = mommy.make(KNOWLEDGE_APP_NAME + '.MicroBlogPost', content=text, posted_on_twitter=True)
        post.category.add(category)
        formated = format_twitter_post(post)
        response = (
            'This is the post text http://some.url.com more text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with... '
            'http://www.vinta.com.br/lessons-learned/this-is-the-post-text-more/'
            ' #Chrome'
        )
        self.assertEqual(formated, response)

    def test_post_format_to_share(self):
        text = (
            'This is the post text http://some.url.com more text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
            'with more text This is the post text with more text This is the post text'
        )
        post = mommy.make(KNOWLEDGE_APP_NAME + '.MicroBlogPost', content=text, posted_on_twitter=True)
        formated = format_twitter_post_to_share(post)
        response = (
            'This+is+the+post+text+http%3A%2F%2Fsome.url.com+more+textwith+more+'
            'text+This+is+the+post+text+with+more+text+This+is+the+post+text'
            'with+more+text+This+is+the+post+text+with+more+text+This+is+the+post+text'
            'with+more+text+This+is+the+post+text+with+more+text...+http%3A%2F%2Fwww.'
            'vinta.com.br%2Flessons-learned%2Fthis-is-the-post-text-more%2F'
        )
        self.assertEqual(formated, response)

