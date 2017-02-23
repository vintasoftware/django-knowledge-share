from django.conf.urls import url

from .endpoints import MicroblogPostRateUpdateAPIView
from .rss_feeds import MicroblogRssFeed
from .views import MicroblogPostView, SlackSlashWebHookView


urlpatterns = [
    url(r'^microblog/integrations/slack-slash/$',
        SlackSlashWebHookView.as_view(), name='microblog-slack-slash'),
    url(r'^microblog/feed/$', MicroblogRssFeed(), name='microblog-feed'),
    url(r'^microblog/(?P<slug>[\w-]+)/$', MicroblogPostView.as_view(), name='microblog-post'),
    url(r'^microblog/(?P<pk>\d+)/rate/$', MicroblogPostRateUpdateAPIView.as_view(), name='microblog-post-rate'),
]
