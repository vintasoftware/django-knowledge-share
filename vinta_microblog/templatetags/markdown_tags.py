import misaka

from django import template

register = template.Library()


@register.filter
def convert_to_html(content):
    html_content = misaka.html(content, extensions=(
        'fenced-code', 'autolink', 'strikethrough',
        'underline', 'highlight', 'quote', 'math', 'no-intra-emphasis'
    ))
    html_content = html_content.replace('<a href', r'<a target="_blank" href')
    return html_content
