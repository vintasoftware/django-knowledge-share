=====
Usage
=====

To use Vinta Microblog in a project, add it to your `INSTALLED_APPS`:

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
