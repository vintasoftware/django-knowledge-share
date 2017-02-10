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


KNOWLEDGE_APP_NAME = _lazy_get_settings('KNOWLEDGE_APP_NAME', str, 'microblog')
KNOWLEDGE_HOST_NAME = _lazy_get_settings('KNOWLEDGE_HOST_NAME', str)
KNOWLEDGE_FEED_TITLE = _lazy_get_settings('KNOWLEDGE_FEED_TITLE', str, 'microblog')
KNOWLEDGE_FEED_LINK = _lazy_get_settings('KNOWLEDGE_FEED_LINK', str, '/microblog/')
KNOWLEDGE_USE_TWITTER = _lazy_get_settings('KNOWLEDGE_USE_TWITTER', bool, True)
