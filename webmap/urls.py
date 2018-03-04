"""URLs for the webmap app."""
from django.conf import settings
from django.conf.urls import include, url

from djgeojson.views import GeoJSONLayerView

from webmap import models, views

from .rest import router


urlpatterns = [
    url(r'^kml/([-\w]+)/$', views.kml_view),
    url(r'^search/([- \w]+)/$', views.search_view),
    url(r'^leaflet-include.js$', views.LeafletIncludeView.as_view(), name='leaflet_include'),
    url(r'^popup/(?P<pk>\d+)/$', views.PopupView.as_view(), name="popup_view"),
    url(r'^geojson$', GeoJSONLayerView.as_view(
        model=models.Poi,
        properties=(
            'marker',
            'popup_url',
            'name',
        ),
    ), name='data'),
]

if getattr(settings, 'REST_ENABLED', False):
    urlpatterns.append(url(r'^', include(router.urls)))
    urlpatterns.append(url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')))
