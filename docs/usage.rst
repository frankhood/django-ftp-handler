=====
Usage
=====

To use FTPHandler in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'ftp_handler.apps.FtpHandlerConfig',
        ...
    )

Add FTPHandler's URL patterns:

.. code-block:: python

    from ftp_handler import urls as ftp_handler_urls


    urlpatterns = [
        ...
        url(r'^', include(ftp_handler_urls)),
        ...
    ]
