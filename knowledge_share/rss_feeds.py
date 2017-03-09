from django.apps import apps
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _

from knowledge_share.conf import KNOWLEDGE_APP_NAME

MicroBlogPost = apps.get_model(KNOWLEDGE_APP_NAME, 'MicroBlogPost')


class MicroblogRssFeed(Feed):
    title = "Lessons Learned"
    link = "/lessons-learned/"
    description = _("Updates on changes and additions to Lessons Learned.")

    def items(self):
        return MicroBlogPost.objects.order_by('-pub_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.get_absolute_url()
