from rest_framework import routers, serializers, viewsets
from .models import Poi, Photo, Property, Marker, Layer
from rest_framework import filters


class PhotoItemSerializer(serializers.ModelSerializer):
    license = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()
    thumb_url = serializers.StringRelatedField()

    class Meta:
        model = Photo
        exclude = ('poi',)


class MarkerItemSerializer(serializers.ModelSerializer):
    layer = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Marker
        fields = ('id', 'slug', 'name', 'layer')


class LayerItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer


class PropertyItemSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()

    class Meta:
        model = Property
        exclude = ('as_filter', 'order', )


class PoiSerializer(serializers.ModelSerializer):
    properties = serializers.StringRelatedField(many=True)
    marker = MarkerItemSerializer(read_only=True)
    status = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()
    photos = PhotoItemSerializer(many=True, read_only=True)
    properties = PropertyItemSerializer(many=True, read_only=True)

    class Meta:
        model = Poi
        exclude = ('properties_cache',)


# ViewSets define the view behavior.
class PoiViewSet(viewsets.ModelViewSet):
    queryset = Poi.visible.all()
    filter_fields = ('author', 'marker__id', 'marker__name', 'properties__id', 'properties__name', 'marker__layer__slug', 'marker__layer__id', 'marker__layer__name')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name', 'desc')
    serializer_class = PoiSerializer


# ViewSets define the view behavior.
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoItemSerializer


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.filter(status__show=True, layer__status__show=True)
    serializer_class = MarkerItemSerializer


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.filter(status__show=True)
    serializer_class = LayerItemSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.filter(status__show=True)
    serializer_class = PropertyItemSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'pois', PoiViewSet)
router.register(r'markers', MarkerViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'layers', LayerViewSet)
