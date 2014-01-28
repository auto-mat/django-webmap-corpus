"""URLs for the webmap app."""
from django.conf.urls import patterns
from webmap import views


urlpatterns = patterns(
    '',
    (r'^kml/([-\w]+)/$', views.kml_view),
    (r'^search/([- \w]+)/$', views.search_view),
)
