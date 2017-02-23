from django.test import TestCase

from model_mommy import mommy

from knowledge_share.conf import KNOWLEDGE_APP_NAME
from knowledge_share.serializers import MicroBlogPostSerializer


class MicroBlogPostSerializerTests(TestCase):

    def setUp(self):
        self.serializer = MicroBlogPostSerializer
        self.microblog_post = mommy.make(
            KNOWLEDGE_APP_NAME + '.MicroBlogPost',
            content='chrome extension'
        )

    def test_serializer_update_positive_rate(self):
        post_serializer = self.serializer(instance=self.microblog_post, data={})
        post_serializer.is_valid()
        microblog_post = post_serializer.save()
        self.assertEqual(microblog_post.positive_rate, 2)

    def test_serializer_data(self):
        post_serializer = self.serializer(instance=self.microblog_post, data={})
        post_serializer.is_valid()
        self.assertEqual(post_serializer.data, {'positive_rate': 1})
