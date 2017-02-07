# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from vinta_microblog.views import MicroblogPostView
from vinta_microblog import urls as vinta_microblog_urls

urlpatterns = [
    url(r'^lessons-learned/(?P<slug>[\w-]+)/$', MicroblogPostView.as_view(), name='microblog-post'),
] + vinta_microblog_urls.urlpatterns
