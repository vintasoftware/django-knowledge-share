# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from knowledge_share import urls as knowledge_share_urls
from knowledge_share.views import MicroblogPostView

urlpatterns = [
    url(r'^lessons-learned/(?P<slug>[\w-]+)/$', MicroblogPostView.as_view(), name='microblog-post'),
] + knowledge_share_urls.urlpatterns[:2]
