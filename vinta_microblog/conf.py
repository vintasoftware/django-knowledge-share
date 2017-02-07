from django.conf import settings

MICROBLOG_APP_NAME = getattr(settings, 'MICROBLOG_APP_NAME', 'microblog')
MICROBLOG_HOST_NAME = settings.MICROBLOG_HOST_NAME
MICROBLOG_FEED_TITLE = getattr(settings, 'MICROBLOG_FEED_TITLE', 'microblog')
MICROBLOG_FEED_LINK = getattr(settings, 'MICROBLOG_FEED_LINK', '/microblog/')
MICROBLOG_USE_TWITTER = getattr(settings, 'MICROBLOG_USE_TWITTER', True)
