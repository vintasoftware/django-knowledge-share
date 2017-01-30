from django.conf.urls import url

from .views import SlackSlashWebHookView
from .rss_feeds import MicroblogRssFeed


urlpatterns = [
    url(r'^microblog/integrations/slack-slash/$',
        SlackSlashWebHookView.as_view(), name='slack-slash'),
    url(r'^microblog/feed/$', MicroblogRssFeed()),
]
