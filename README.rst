=============================
FTPHandler
=============================

.. image:: https://badge.fury.io/py/ftp-handler.svg/?style=flat-square
    :target: https://badge.fury.io/py/ftp-handler

.. image:: https://readthedocs.org/projects/pip/badge/?version=latest&style=flat-square
    :target: https://ftp-handler.readthedocs.io/en/latest/

.. image:: https://img.shields.io/coveralls/github/frankhood/ftp-handler/main?style=flat-square
    :target: https://coveralls.io/github/frankhood/ftp-handler?branch=main
    :alt: Coverage Status

Your project description goes here

Documentation
-------------

The full documentation is at https://ftp-handler.readthedocs.io.

Quickstart
----------

Install FTPHandler::

    pip install ftp-handler

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'ftp_handler',
        ...
    )


Features
--------

Send files in any format to a remote server via ftp/sftp in two ways:

* Inheriting FTPHandler class and customizing port, server, username, password and remote directory path
* Instantiating FTPHandler class passing port, server, username, password and remote directory path

.. code-block:: python

    @dataclass
    class YourFTPHandler(FTPHandler):
        ftp_server = "sftp.test.com"
        ftp_port = 22
        ftp_username = 'Username'
        ftp_password = 'Password'
        is_sftp = True
        remote_path = 'Remote path of the directory'


    def send_document_on_ftp_with_inheritance(file: ContentFile, filename):
        content_file = file
        handler = YourFTPHandler()
        try:
            handler.send_to_ftp_server(
                content_file,
                filename=filename
            )
            logger.info(f"{filename} successfully uploaded on {handler.ftp_server} server.")
        except Exception as exc:
            logger.exception(f"{filename} not uploaded on {handler.ftp_server} server.")
            raise exc


    def send_document_on_ftp_without_inheritance(file: ContentFile, filename):
        content_file = file
        handler = FTPHandler(
            ftp_server="sftp.test.com",
            ftp_port=22,
            ftp_username='Username',
            ftp_password='Password',
            is_sftp=True,
            remote_path='Remote path of the directory'
        )
        try:
            handler.send_to_ftp_server(
                content_file,
                filename=filename
            )
            logger.info(f"{filename} successfully uploaded on {handler.ftp_server} server.")
        except Exception as exc:
            logger.exception(f"{filename} not uploaded on {handler.ftp_server} server.")
            raise exc

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
