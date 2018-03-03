# -*- encoding: utf-8 -*-
"""
Python setup file for the webmap app.

In order to register your app at pypi.python.org, create an account at
pypi.python.org and login, then register your new app like so:

    python setup.py register

If your name is still free, you can now make your first release but first you
should check if you are uploading the correct files:

    python setup.py sdist

Inspect the output thoroughly. There shouldn't be any temp files and if your
app includes staticfiles or templates, make sure that they appear in the list.
If something is wrong, you need to edit MANIFEST.in and run the command again.

If all looks good, you can make your first release:

    python setup.py sdist upload

For new releases, you need to bump the version number in
webmap/__init__.py and re-run the above command.

For more information on creating source distributions, see
http://docs.python.org/2/distutils/sourcedist.html

"""
import os
import sys

from setuptools import find_packages, setup

import webmap as app

# Make sure the django.mo file also exists:
try:
    os.chdir('webmap')
    from django.core import management
    management.call_command('compilemessages', stdout=sys.stderr, verbosity=1)
except ImportError:
    if 'sdist' in sys.argv:
        raise
finally:
    os.chdir('..')


dev_requires = [
    'flake8',
    'django_nose',
    'django_jasmine',
]

dependency_links = [
]

install_requires = [
    'django',
    'django-colorful',
    'django-author>=0.2',
    'django-admin-sortable2',
    'psycopg2',
    'easy_thumbnails',
    'django-import-export',
    'django-finegrained-permissions',
    'django-constance[database]',
    'pillow',
    'djangorestframework',
    'django-filter',
    'django-gpxpy',
    'django-leaflet',
    'django-filters',
]


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="django-webmap-corpus",
    version=app.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='GNU Affero General Public License, Version 3.0',
    platforms=['OS Independent'],
    keywords='django, map',
    author='Petr Dlouhý',
    author_email='petr.dlouhy@email.cz',
    url="https://github.com/auto-mat/django-webmap-corpus",
    packages=find_packages(),
    include_package_data=True,
    dependency_links=dependency_links,
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
