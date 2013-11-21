"""URLs for the django_webmap_corpus app."""
from django.conf.urls import patterns, url
from django_webmap_corpus import views


urlpatterns = patterns(
    '',
    (r'^kml/([-\w]+)/$', views.kml_view),
)
