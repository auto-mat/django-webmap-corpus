"""URLs for the webmap app."""
from django.conf import settings
from django.conf.urls import include, url

from webmap import views

from .rest import router


urlpatterns = [
    url(r'^kml/([-\w]+)/$', views.kml_view),
    url(r'^search/([- \w]+)/$', views.search_view),
]

if getattr(settings, 'REST_ENABLED', False):
    urlpatterns.append(url(r'^', include(router.urls)))
    urlpatterns.append(url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')))
