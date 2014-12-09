"""URLs for the webmap app."""
from django.conf.urls import patterns, include, url
from webmap import views
from rest import router


urlpatterns = patterns(
    '',
    (r'^kml/([-\w]+)/$', views.kml_view),
    (r'^search/([- \w]+)/$', views.search_view),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
