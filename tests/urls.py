# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from knowledge_share.views import MicroblogPostView
from knowledge_share import urls as knowledge_share_urls

urlpatterns = [
    url(r'^lessons-learned/(?P<slug>[\w-]+)/$', MicroblogPostView.as_view(), name='microblog-post'),
] + knowledge_share_urls.urlpatterns[:2]
