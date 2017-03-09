import misaka
from django import template

register = template.Library()


@register.filter
def format_post(post):
    from knowledge_share.twitter_helpers import format_twitter_post_to_share
    return format_twitter_post_to_share(post)


@register.filter
def convert_to_html(content):
    html_content = misaka.html(content, extensions=(
        'fenced-code', 'autolink', 'strikethrough',
        'underline', 'highlight', 'quote', 'math', 'no-intra-emphasis'
    ))
    html_content = html_content.replace('<a href', r'<a target="_blank" href')
    return html_content
