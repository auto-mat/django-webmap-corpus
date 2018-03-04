"""URLs for the webmap app."""
from django.conf import settings
from django.conf.urls import include, url

from webmap import views

from .rest import router


urlpatterns = [
    url(r'^kml/([-\w]+)/$', views.kml_view),
    url(r'^search/([- \w]+)/$', views.search_view),
    url(r'^leaflet-include.js$', views.LeafletIncludeView.as_view(), name='leaflet_include'),
    url(r'^popup/(?P<pk>\d+)/$', views.PopupView.as_view(), name="popup_view"),
    url(r'^geojson/(?P<layer_slug>[^&]+)/$', views.WebmapGeoJsonView.as_view(), name='data'),
]

if getattr(settings, 'REST_ENABLED', False):
    urlpatterns.append(url(r'^', include(router.urls)))
    urlpatterns.append(url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')))
