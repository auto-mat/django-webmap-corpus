from rest_framework import routers, serializers, viewsets
from models import Poi, Photo


class PhotoItemSerializer(serializers.ModelSerializer):
    license = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()

    class Meta:
        model = Photo


class PoiSerializer(serializers.ModelSerializer):
    properties = serializers.StringRelatedField(many=True)
    marker = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()
    photos = PhotoItemSerializer(many=True, read_only=True)

    class Meta:
        model = Poi


# ViewSets define the view behavior.
class PoiViewSet(viewsets.ModelViewSet):
    queryset = Poi.objects.all()
    serializer_class = PoiSerializer


# ViewSets define the view behavior.
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoItemSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'pois', PoiViewSet)
