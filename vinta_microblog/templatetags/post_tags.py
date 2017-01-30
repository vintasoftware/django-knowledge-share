from django import template

from vinta_microblog.twitter_helpers import format_twitter_post_to_share

register = template.Library()


@register.filter
def format_post(post):
    return format_twitter_post_to_share(post)
