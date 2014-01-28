"""URLs for the webmap app."""
from django.conf.urls import patterns
from webmap import views, search_view


urlpatterns = patterns(
    '',
    (r'^kml/([-\w]+)/$', views.kml_view),
    (r'^search/([- \w]+)/$', search_view),
)
