# -*- coding: utf-8 -*-
# admin.py

from django.conf import settings # needed if we use the GOOGLE_MAPS_API_KEY from settings

# Import the admin site reference from django.contrib.admin
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
#from import_export.admin import ImportExportModelAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from constance import config
import fgp
from django.core.urlresolvers import reverse

# Grab the Admin Manager that automaticall initializes an OpenLayers map
# for any geometry field using the in Google Mercator projection with OpenStreetMap basedata
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.geos import Point

# Note, another simplier manager that does not reproject the data on OpenStreetMap is available
# with from `django.contrib.gis.admin import GeoModelAdmin`

# Finally, import our model from the working project
# the geographic_admin folder must be on your python path
# for this import to work correctly
from models import *

USE_GOOGLE_TERRAIN_TILES = False

class UserAdmin(UserAdmin):
    list_display = ('__unicode__', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'get_groups', 'get_user_permissions')

    def get_groups(self, obj):
        if obj:
            return ", ".join([group.name for group in obj.groups.all()])

    def get_user_permissions(self, obj):
        if obj:
            return ", ".join([user_permission.name for user_permission in obj.user_permissions.all()])


class SectorFilter(SimpleListFilter):
    title = _(u"sector")
    parameter_name = u"sector"

    def lookups(self, request, model_admin):
        return [("outer", _(u"Out of sectors"))] + [(sector.slug, sector.name) for sector in Sector.objects.all()]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == "outer":
            for sector in Sector.objects.all():
                queryset = queryset.exclude(geom__contained = sector.geom)
            return queryset
        return queryset.filter(geom__contained = Sector.objects.get(slug = self.value()).geom)

class PoiStatusFilter(SimpleListFilter):
    title = _(u"all statuses")
    parameter_name = u"statuses"

    def lookups(self, request, model_admin):
        return ((None, _(u"Visible")),
                ('all', _('All')),
                ("unvisible", _(u"Unvisible")))

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        if not self.value() or self.value() == "visible":
            return queryset.filter(Q(status__show_to_mapper = True) & Q(marker__status__show_to_mapper = True) & Q(marker__layer__status__show_to_mapper = True))
        if self.value() == "unvisible":
            return queryset.exclude(Q(status__show_to_mapper = True) & Q(marker__status__show_to_mapper = True) & Q(marker__layer__status__show_to_mapper = True))

class PhotoInline(admin.TabularInline):
    model = Photo
    readonly_fields = ('image_tag', 'author', 'updated_by')

@fgp.enforce
class PoiAdmin(OSMGeoAdmin):#, ImportExportModelAdmin):
    model = Poi
    list_display = ['name','status', 'marker', 'properties_list', 'last_modification', 'address', 'url', 'desc', 'id' ]
    list_filter = (PoiStatusFilter, 'status', SectorFilter, 'marker__layer', 'marker',)
    exclude = ('properties_cache', )
    readonly_fields = ("created_at", "last_modification", "author", "updated_by")
    raw_id_fields = ('marker',)
    search_fields = ('name',)
    ordering = ('name',)
    save_as = True
    search_fields = ['name']
    list_select_related = True
    filter_horizontal = ('properties',)
    inlines = [PhotoInline]
    list_max_show_all = 10000

    if USE_GOOGLE_TERRAIN_TILES:
      map_template = 'gis/admin/google.html'
      extra_js = ['http://openstreetmap.org/openlayers/OpenStreetMap.js', 'http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s' % settings.GOOGLE_MAPS_API_KEY]
    else:
      pass # defaults to OSMGeoAdmin presets of OpenStreetMap tiles

    # Default GeoDjango OpenLayers map options
    # Uncomment and modify as desired
    # To learn more about this jargon visit:
    # www.openlayers.org
    
    def get_form(self, request, obj=None, **kwargs):
         pnt = Point(config.MAP_BASELON, config.MAP_BASELAT, srid=4326)
         pnt.transform(900913)
         self.default_lon, self.default_lat = pnt.coords

         if not request.user.is_superuser and request.user.has_perm(u'mapa.can_only_own_data_only') and obj and obj.author != request.user:
             self.fields = ('name', )
             self.readonly_fields = ('name', )
         else:
             self.fields = PoiAdmin.fields
             self.readonly_fields = PoiAdmin.readonly_fields
         return super(PoiAdmin, self).get_form(request, obj, **kwargs)

    default_zoom = 12
    scrollable = False
    map_width = 700
    map_height = 500
    map_srid = 900913

class SectorAdmin(OSMGeoAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',) } # slug se automaticky vytvari z nazvu
    if USE_GOOGLE_TERRAIN_TILES:
      map_template = 'gis/admin/google.html'
      extra_js = ['http://openstreetmap.org/openlayers/OpenStreetMap.js', 'http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s' % settings.GOOGLE_MAPS_API_KEY]
    else:
      pass # defaults to OSMGeoAdmin presets of OpenStreetMap tiles

    def get_form(self, request, obj=None, **kwargs):
         pnt = Point(config.MAP_BASELON, config.MAP_BASELAT, srid=4326)
         pnt.transform(900913)
         self.default_lon, self.default_lat = pnt.coords
         return super(SectorAdmin, self).get_form(request, obj, **kwargs)

    default_zoom = 12
    scrollable = False
    map_width = 700
    map_height = 500
    map_srid = 900913

class MarkerInline(admin.TabularInline):
    model = Marker

class LayerAdmin(admin.ModelAdmin): #ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('name',) } # slug se automaticky vytvari z nazvu
    list_display = ['name', 'slug', 'status', 'order']
    inlines = [MarkerInline]

class MapaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',) } # slug se automaticky vytvari z nazvu

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'as_filter', 'status', 'order')
    prepopulated_fields = {'slug': ('name',) } # slug se automaticky vytvari z nazvu
    model = Property

class MarkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'layer', 'minzoom', 'status', 'default_icon_image', 'id', 'poi_count')
    list_filter = ('layer','status',)
    search_fields = ('name', 'desc',)
    readonly_fields = ('poi_count',)

    def default_icon_image(self, obj):
        if obj.default_icon:
            return '<img src="%s"/>' % obj.default_icon.url
    default_icon_image.short_description = _("icon")
    default_icon_image.allow_tags = True

    def has_change_permission(self, request, obj = None):
        if obj == None and request.user.has_perm(u'webmap.can_only_view'):
            return True
        return super(MarkerAdmin, self).has_change_permission(request, obj)

    def poi_count(self, obj):
        url = reverse('admin:webmap_poi_changelist')
        return '<a href="{0}?marker__id__exact={1}&amp;statuses=all">{2}</a>'.format(url, obj.id, obj.pois.count())
    poi_count.short_description = _("count")
    poi_count.allow_tags = True

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'show', 'show_to_mapper')

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')
    
admin.site.register(Poi   , PoiAdmin   )
admin.site.register(Layer, LayerAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Marker, MarkerAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(License, LicenseAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
