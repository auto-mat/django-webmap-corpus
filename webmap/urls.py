"""URLs for the webmap app."""
from django.conf.urls import patterns, url
from webmap import views


urlpatterns = patterns(
    '',
    (r'^kml/([-\w]+)/$', views.kml_view),
)
