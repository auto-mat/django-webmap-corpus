.. image:: https://travis-ci.org/auto-mat/django-webmap-corpus.svg?branch=master
    :target: https://travis-ci.org/auto-mat/django-webmap-corpus
.. image:: https://coveralls.io/repos/auto-mat/django-webmap-corpus/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/auto-mat/django-webmap-corpus?branch=master

Django webmap corpus
====================

Corpus for making web map applications.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-webmap-corpus

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+https://github.com/PetrDlouhy/django-webmap-corpus.git#egg=webmap

Add ``webmap`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'author',
        'colorful',
        'adminsortable2',
        'django.contrib.gis',
        'constance.backends.database',
        'constance',
        'import_export',
        'webmap',
        'rest_framework',
    )

Add Author middleware

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...,
        'author.middlewares.AuthorDefaultBackendMiddleware',
    )

Add Constance settings

.. code-block:: python

    CONSTANCE_APP_NAME = "webmap"
    CONSTANCE_CONFIG = {
        'MAP_BASELON': (14.4211, u'zeměpisná délka základní polohy mapy'),
        'MAP_BASELAT': (50.08741, u'zeměpisná délka základní polohy mapy'),
        'MAP_BOUNDS': ("14.22, 49.95, 14.8, 50.18", u'hranice zobrazení mapy'),
        'DEFAULT_STATUS_ID': (2, u'id defaultního statusu'),
    }
    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

Add the ``webmap`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^webmap/', include('webmap.urls')),
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate webmap

Note: If you don't have Constance migrated yet, remove the 'webmap' line from INSTALLED_APPS, then migrate Constance and then the line re-add and migrate again.


Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-webmap-corpus
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
