=============================
Django Knowledge Share
=============================

.. image:: https://badge.fury.io/py/django-knowledge-share.svg
    :target: https://badge.fury.io/py/django-knowledge-share

.. image:: https://travis-ci.org/vintasoftware/django-knowledge-share.svg?branch=master
    :target: https://travis-ci.org/vintasoftware/django-knowledge-share

.. image:: https://codecov.io/gh/vintasoftware/django-knowledge-share/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/vintasoftware/django-knowledge-share

Microblog app used to share quick knowledge. This code powers Vinta's lessons learned
running at http://www.vinta.com.br/lessons-learned/.

The posts are created via slack using a custom command and are automatically posted on twitter.

Quickstart
----------

Install Django Knowledge Share::

    pip install django-knowledge-share

Create an app for your microblog::

    python manage.py startapp microblog

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        "microblog",
        "knowledge_share",
        ...
    )

In your urls.py add the urls entry::

    url(r'^', include('knowledge_share.urls', namespace='microblog')),

In your microblog/models.py create your models by inheriting from the abstract models:

.. code-block:: python

    # customize those models as needed
    from knowledge_share import models as knowledge_share_abstract_models


    class MicroBlogPost(knowledge_share_abstract_models.MicroBlogPostBase):
        pass


    class MicroBlogCategory(knowledge_share_abstract_models.MicroBlogCategoryBase):
        pass

Then create and run your migrations::

    python manage.py makemigrations
    python manage.py migrate


Documentation
-------------

Models
~~~~~~

You can see the available models and it's fields `here
<knowledge_share/models.py>`_. They are all abstract and you need to create an instance of it (see Quickstart section).

Slack Integration
~~~~~~~~~~~~~~~~~

Create a custom command in this page: `https://my.slack.com/services/new/slash-commands <https://my.slack.com/services/new/slash-commands>`_.

Set the url to your slack endpoint, by default https://yoursite.com/microblog/integrations/slack-slash/
Copy the generated token and add to your settings.py as "SLACK_TOKEN='your-token'".
To send a new post use ``/yourcommand This is a blog post content [Category, Another Category]``

Twitter Integration
~~~~~~~~~~~~~~~~~~~

You will need to set the following settings using your twitter data::

    TWITTER_API_KEY
    TWITTER_API_SECRET
    TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_TOKEN_SECRET

Whenever new posts are created it will be posted to twitter.

Template tags
~~~~~~~~~~~~~

Whenever you are showing the content of the post you should use::

    {% load microblog %}

    {{ post.content|convert_to_html }}

If you want to create a link with the content to be shared you can use::

    {% load microblog %}

    <a href="https://twitter.com/intent/tweet?text={{ post|format_post }}">
        Share on twitter
    </a>

RSS Feed
~~~~~~~~

There is a RSS feed served by default at /microblog/feed/.

Configuration
~~~~~~~~~~~~~

The following configurations are available:

.. code-block:: python

    # settings.py

    # name of the app created with your microblog's models
    KNOWLEDGE_APP_NAME = 'microblog'
    # the title of the rss feed (available at: /microblog/feed/)
    KNOWLEDGE_FEED_TITLE = 'microblog'
    # the link of the feed
    KNOWLEDGE_FEED_LINK = '/microblog/'
    # Either to use twitter or not
    KNOWLEDGE_USE_TWITTER = True


Running Tests
-------------

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
