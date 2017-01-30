# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from vinta_microblog.urls import urlpatterns as vinta_microblog_urls

urlpatterns = [
    url(r'^', include(vinta_microblog_urls, namespace='vinta_microblog')),
]
