"""URLs for the webmap app."""
from django.conf.urls import patterns, include, url
from webmap import views
from .rest import router
from django.conf import settings


urlpatterns = patterns(
    '',
    (r'^kml/([-\w]+)/$', views.kml_view),
    (r'^search/([- \w]+)/$', views.search_view),
)

if getattr(settings, 'REST_ENABLED', False):
    urlpatterns.append(url(r'^', include(router.urls)))
    urlpatterns.append(url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')))
