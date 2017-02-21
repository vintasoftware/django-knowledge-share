import json

from django.apps import apps

from rest_framework.generics import UpdateAPIView

from knowledge_share.conf import KNOWLEDGE_APP_NAME
from knowledge_share.serializers import MicroBlogPostSerializer


MicroBlogPost = apps.get_model(KNOWLEDGE_APP_NAME, 'MicroBlogPost')


class MicroblogPostRateUpdateAPIView(UpdateAPIView):
    serializer_class = MicroBlogPostSerializer
    queryset = MicroBlogPost.objects.select_for_update().all()

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(MicroblogPostRateUpdateAPIView, self).finalize_response(
            request, response, *args, **kwargs)

        post_id = int(kwargs['pk'])

        posts_id = request.COOKIES.get('posts_id')
        if posts_id:
            posts_id = json.loads(posts_id)
            posts_id['posts_id'].append(post_id)
            posts_id_json = json.dumps(posts_id)
            response.set_cookie('posts_id', posts_id_json)
        else:
            posts_id_json = json.dumps({'posts_id': [post_id]})
            response.set_cookie('posts_id', posts_id_json)

        return response
