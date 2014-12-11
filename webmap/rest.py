from rest_framework import routers, serializers, viewsets
from models import Poi, Photo, Property, Marker


class PhotoItemSerializer(serializers.ModelSerializer):
    license = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()

    class Meta:
        model = Photo
        exclude = ('poi',)

class MarkerItemSerializer(serializers.ModelSerializer):
    layer = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Marker
        fields = ('id', 'slug', 'name', 'layer')

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
    serializer_class = PoiSerializer


# ViewSets define the view behavior.
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoItemSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'pois', PoiViewSet)
