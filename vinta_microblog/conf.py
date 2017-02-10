from django.utils.functional import lazy

obj = object()


def _call_getattr(opt, value):
    from django.conf import settings
    if value is obj:
        return getattr(settings, opt)
    return getattr(settings, opt, value)


def _lazy_get_settings(opt, ttype, default_value=obj):
    return lazy(_call_getattr, ttype)(opt, default_value)

# Lazyly read configurations to allow @override_settings


MICROBLOG_APP_NAME = _lazy_get_settings('MICROBLOG_APP_NAME', str, 'microblog')
MICROBLOG_HOST_NAME = _lazy_get_settings('MICROBLOG_HOST_NAME', str)
MICROBLOG_FEED_TITLE = _lazy_get_settings('MICROBLOG_FEED_TITLE', str, 'microblog')
MICROBLOG_FEED_LINK = _lazy_get_settings('MICROBLOG_FEED_LINK', str, '/microblog/')
MICROBLOG_USE_TWITTER = _lazy_get_settings('MICROBLOG_USE_TWITTER', bool, True)
