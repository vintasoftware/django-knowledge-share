import logging
import re

from bs4 import BeautifulSoup
from django.conf import settings

from knowledge_share.conf import KNOWLEDGE_HOST_NAME
from knowledge_share.templatetags.microblog import convert_to_html
from six.moves.urllib.parse import quote_plus
from tapioca.exceptions import ClientError
from tapioca_twitter import Twitter

logger = logging.getLogger(__name__)

TWITTER_MAX_CHARACTER = 140
TWITTER_URL_SHORTENER_SIZE = 23
ELLIPSIS = '... '
URL_REGEX = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
MAX_TWEET_SIZE = TWITTER_MAX_CHARACTER - (TWITTER_URL_SHORTENER_SIZE + len(ELLIPSIS))


def word_len(word):
    word_size = len(word)
    if re.findall(URL_REGEX, word):
        word_size = TWITTER_URL_SHORTENER_SIZE
    return word_size


def create_content(post_words, post_url, post_category):
    tweet_size = 0
    tweet = ''
    category_size = len(post_category) + 1 if post_category else 0
    for i, word in enumerate(post_words):
        word_size = word_len(word)
        will_be_size = tweet_size + word_size + 1
        if will_be_size > MAX_TWEET_SIZE - category_size:
            tweet += ELLIPSIS
            break

        if tweet:
            tweet += ' '
            tweet_size += 1

        tweet += word
        tweet_size += word_size

    fmt_tweet = '{}{}'.format(tweet, post_url)
    if category_size:
        fmt_tweet = '{} {}'.format(fmt_tweet, post_category)
    return fmt_tweet


def format_twitter_post(post):
    # Markdown to text
    html_post_content = convert_to_html(post.content)
    text_post_content = BeautifulSoup(html_post_content, "lxml").text

    # Getting microblog post link
    base_url = KNOWLEDGE_HOST_NAME.rstrip('/')
    post_url = post.get_absolute_url().lstrip('/')
    full_post_url = '{}/{}'.format(base_url, post_url)

    post_words = text_post_content.split(' ')
    category = post.category.first()
    category_hashtag = ''
    if category:
        category_hashtag = category.hashtag
    tweet_content = create_content(post_words, full_post_url, category_hashtag)
    return tweet_content


def format_twitter_post_to_share(post):
    return quote_plus(format_twitter_post(post))


def post_microblog_post_on_twitter(microblog_post):
    api = Twitter(
        api_key=settings.TWITTER_API_KEY,
        api_secret=settings.TWITTER_API_SECRET,
        access_token=settings.TWITTER_ACCESS_TOKEN,
        access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    post_content = format_twitter_post(microblog_post)
    try:
        api.statuses_update().post(params={'status': post_content})
        microblog_post.posted_on_twitter = True
        microblog_post.save()
    except ClientError:
        logger.error(
            "Tried to post a microblog post on Twitter but got a ClientError, "
            "check your twitter keys.")
        raise
