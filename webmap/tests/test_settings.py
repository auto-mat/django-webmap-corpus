# -*- coding: utf-8 -*-

"""Settings that need to be set in order to run the tests."""
import os
import sys

from django.utils.translation import ugettext_lazy as _

DEBUG = True

SITE_ID = 1

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'),
)
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(APP_ROOT, 'tests/test_app/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': {
                "django.contrib.auth.context_processors.auth",
                'django.contrib.messages.context_processors.messages',
            },
        },
    },
]

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'author.middlewares.AuthorDefaultBackendMiddleware',
)

MIDDLEWARE_CLASSES = MIDDLEWARE

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
    'leaflet',
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

CONSTANCE_APP_NAME = "webmap"
CONSTANCE_CONFIG = {
    'MAP_BASELON': (14.4211, u'zeměpisná délka základní polohy mapy'),
    'MAP_BASELAT': (50.08741, u'zeměpisná délka základní polohy mapy'),
    'MAP_BOUNDS': ("14.22, 49.95, 14.8, 50.18", u'hranice zobrazení mapy'),
    'DEFAULT_STATUS_ID': (2, u'id defaultního statusu'),
    'ABOUT_MAP': ("Lorem ipsum", u'info o mapě'),
    'MAP_NEWS': ("Lorem ipsum", u'novinky mapy'),
}
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (50.0866699218750000, 14.4387817382809995),
    'TILES': [
        (
            _(u'cyklomapa'),
            'http://tiles.prahounakole.cz/{z}/{x}/{y}.png',
            {'attribution': u'&copy; přispěvatelé <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}),
        (
            _(u'Všeobecná mapa'),
            'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {'attribution': u'&copy; přispěvatelé <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}),
    ],
    'DEFAULT_ZOOM': 8,
    'MIN_ZOOM': 8,
    'MAX_ZOOM': 18,
    'SPATIAL_EXTENT': [11.953, 48.517, 19.028, 51.097],
}

REST_ENABLED = True
