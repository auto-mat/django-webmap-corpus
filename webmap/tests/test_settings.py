"""Settings that need to be set in order to run the tests."""
import os
import sys

DEBUG = True

SITE_ID = 1

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), APP_ROOT, '..')))

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'travis_ci_test',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    },
}

ROOT_URLCONF = 'webmap.tests.urls'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(APP_ROOT, '../app_static')
MEDIA_ROOT = os.path.join(APP_ROOT, '../app_media')
STATICFILES_DIRS = (
    os.path.join(APP_ROOT, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(APP_ROOT, 'tests/test_app/templates'),
)

MIDDLEWARE_CLASSES = (
    'author.middlewares.AuthorDefaultBackendMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'author.middlewares.AuthorDefaultBackendMiddleware',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django_jasmine',
    'django_nose',
    'author',
    'colorful',
    'easy_thumbnails',
    'adminsortable2',
    'django.contrib.gis',
    'constance.backends.database',
    'constance',
    'import_export',
    'rest_framework',
    'webmap',
    'test_app',
]

SECRET_KEY = 'foobar'
