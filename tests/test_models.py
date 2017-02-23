from django.test import TestCase

from model_mommy import mommy

from knowledge_share.conf import KNOWLEDGE_APP_NAME


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
