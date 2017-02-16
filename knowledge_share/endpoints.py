from django.apps import apps

from rest_framework.generics import UpdateAPIView

from knowledge_share.conf import KNOWLEDGE_APP_NAME
from knowledge_share.serializers import MicroBlogPostSerializer


MicroBlogPost = apps.get_model(KNOWLEDGE_APP_NAME, 'MicroBlogPost')


class MicroBlogPostRateUpdateAPIView(UpdateAPIView):
    serializer_class = MicroBlogPostSerializer
    queryset = MicroBlogPost.objects.select_for_update().all()
