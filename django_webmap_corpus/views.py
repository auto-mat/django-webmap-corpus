"""Views for the django_webmap_corpus app."""
# from django.views.generic import TemplateView

from django_webmap_corpus import models
from django.views.decorators.gzip import *
from django.views.decorators.cache import never_cache, cache_page
from django.shortcuts import get_object_or_404
from django.contrib.gis.shortcuts import render_to_kml

@gzip_page
@never_cache              # don't cache KML in browsers
@cache_page(24 * 60 * 60) # cache in memcached for 24h
def kml_view(request, layer_name):
    # find layer by slug or throw 404
    v = get_object_or_404(models.Layer, slug=layer_name, status__show=True)

    # all enabled pois in this layer
    points = models.Poi.visible.filter(marker__layer=v).kml()
    return render_to_kml("django_webmap_corpus/gis/kml/layer.kml", { 'places' : points})

