=============================
Vinta Microblog
=============================

.. image:: https://badge.fury.io/py/vinta-microblog.svg
    :target: https://badge.fury.io/py/vinta-microblog

.. image:: https://travis-ci.org/vintasoftware/vinta-microblog.svg?branch=master
    :target: https://travis-ci.org/vintasoftware/vinta-microblog

.. image:: https://codecov.io/gh/vintasoftware/vinta-microblog/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/vintasoftware/vinta-microblog

Microblog app used by vinta's site.

Documentation
-------------

The full documentation is at https://vinta-microblog.readthedocs.io.

Quickstart
----------

Install Vinta Microblog::

    pip install vinta-microblog

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'vinta_microblog.apps.VintaMicroblogConfig',
        ...
    )

Add Vinta Microblog's URL patterns:

.. code-block:: python

    from vinta_microblog import urls as vinta_microblog_urls


    urlpatterns = [
        ...
        url(r'^', include(vinta_microblog_urls)),
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
