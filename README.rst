=============================
Django Knowledge Share
=============================

.. image:: https://badge.fury.io/py/django-knowledge-share.svg
    :target: https://badge.fury.io/py/django-knowledge-share

.. image:: https://travis-ci.org/vintasoftware/django-knowledge-share.svg?branch=master
    :target: https://travis-ci.org/vintasoftware/django-knowledge-share

.. image:: https://codecov.io/gh/vintasoftware/django-knowledge-share/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/vintasoftware/django-knowledge-share

Microblog app used to share quick knowledge.

Documentation
-------------

Quickstart
----------

Install Django Knowledge Share::

    pip install django-knowledge-share

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'knowledge_share.apps.KnowledgeShareConfig',
        ...
    )

Add Django Knowledge Share's URL patterns:

.. code-block:: python

    from knowledge_share import urls as knowledge_share_urls


    urlpatterns = [
        ...
        url(r'^', include(knowledge_share_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

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
