Django webmap corpus
============

Corpus for making web map applications.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-webmap-corpus

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://https://github.com/PetrDlouhy/django-webmap-corpus.git#egg=django_webmap_corpus

TODO: Describe further installation steps (edit / remove the examples below):

Add ``django_webmap_corpus`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'django_webmap_corpus',
    )

Add the ``django_webmap_corpus`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^webmap/', include('django_webmap_corpus.urls')),
    )

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load django_webmap_corpus_tags %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate django_webmap_corpus


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
