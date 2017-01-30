from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _
from django.apps import apps

MicroBlogPost = apps.get_model('microblog', 'MicroBlogPost')


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
        return item.get_slug_path()
