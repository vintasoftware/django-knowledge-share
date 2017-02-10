from django.conf.urls import url

from .views import SlackSlashWebHookView, MicroblogPostView
from .rss_feeds import MicroblogRssFeed


urlpatterns = [
    url(r'^microblog/integrations/slack-slash/$',
        SlackSlashWebHookView.as_view(), name='microblog-slack-slash'),
    url(r'^microblog/feed/$', MicroblogRssFeed(), name='microblog-feed'),
    url(r'^microblog/(?P<slug>[\w-]+)/$', MicroblogPostView.as_view(), name='microblog-post'),
]
