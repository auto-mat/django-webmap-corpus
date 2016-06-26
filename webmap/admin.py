# -*- coding: utf-8 -*-
# admin.py

# Import the admin site reference from django.contrib.admin
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import ugettext_lazy as _
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib.auth.admin import UserAdmin, User
from django.contrib.gis.shortcuts import render_to_kml
from django.db.models import Q, Count
from constance.admin import config
from leaflet.admin import LeafletGeoAdmin
import fgp
from django.core.urlresolvers import reverse
from .models import GpxPoiForm, Poi, Photo, PhotoAdminForm, Marker, Property, LegendAdminForm, Legend, Sector, Status, License, BaseLayer, OverlayLayer, MapPreset


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'get_groups', 'get_user_permissions')

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
        self.model_admin = model_admin
        return [("outer", _(u"Out of sectors"))] + [(sector.slug, sector.name) for sector in Sector.objects.all()]

    def queryset(self, request, queryset):
        prefix = ""
        if isinstance(self.model_admin, PhotoAdmin):
            prefix = "poi__"

        if not self.value():
            return queryset
        if self.value() == "outer":
            for sector in Sector.objects.all():
                qfilter = {}
                qfilter[prefix + 'geom__bboverlaps'] = sector.geom  # was intersects, but does not work with GeometryCollection
                queryset = queryset.exclude(**qfilter)
            return queryset
        qfilter = {}
        qfilter[prefix + 'geom__bboverlaps'] = Sector.objects.get(slug=self.value()).geom
        return queryset.filter(**qfilter)


class PoiStatusFilter(SimpleListFilter):
    title = _(u"all statuses")
    parameter_name = u"statuses"

    def lookups(self, request, model_admin):
        return ((None, _(u"Visible")),
                ('all', _('All')),
                ("unvisible", _(u"Invisible")))

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
            return queryset.filter(Q(status__show_to_mapper=True) & Q(marker__status__show_to_mapper=True) & Q(marker__layer__status__show_to_mapper=True))
        if self.value() == "unvisible":
            return queryset.exclude(Q(status__show_to_mapper=True) & Q(marker__status__show_to_mapper=True) & Q(marker__layer__status__show_to_mapper=True))


class PhotoInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Photo
    form = PhotoAdminForm
    extra = 0
    readonly_fields = ('author', 'updated_by', 'created_at', 'last_modification')


def export_kml(modeladmin, request, queryset):
    points = queryset.kml()
    return render_to_kml("webmap/gis/kml/layer.kml", {'places': points})


@fgp.enforce
class PoiAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    model = Poi
    form = GpxPoiForm
    list_display = ['__str__', 'status', 'marker', 'properties_list', 'last_modification', 'address', 'url', 'desc', 'id', 'photo_count']
    list_filter = (PoiStatusFilter, 'status', SectorFilter, 'marker__layer', 'marker', 'properties')
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
    actions = [export_kml, ]

    def get_form(self, request, obj=None, **kwargs):
        self.settings_overrides = {
            'DEFAULT_CENTER': (config.MAP_BASELAT, config.MAP_BASELON),
            'DEFAULT_ZOOM': 12,
        }

        if not request.user.is_superuser and request.user.has_perm(u'mapa.can_only_own_data_only') and obj and obj.author != request.user:
            self.fields = ('name', )
            self.readonly_fields = ('name', )
        else:
            self.fields = PoiAdmin.fields
            self.readonly_fields = PoiAdmin.readonly_fields
        return super(PoiAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super(PoiAdmin, self).get_queryset(request)
        qs = qs.annotate(Count('photos'))
        return qs

    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.admin_order_field = 'photos__count'


class SectorAdmin(LeafletGeoAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # automatically make slug from name

    def get_form(self, request, obj=None, **kwargs):
        self.settings_overrides = {
            'DEFAULT_CENTER': (config.MAP_BASELAT, config.MAP_BASELON),
            'DEFAULT_ZOOM': 12,
        }
        return super(SectorAdmin, self).get_form(request, obj, **kwargs)


class MarkerInline(admin.TabularInline):
    model = Marker
    extra = 0


class OverlayLayerAdmin(SortableAdminMixin, ImportExportModelAdmin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # automatically make slug from name
    list_display = ['name', 'slug', 'status', 'order', 'enabled']
    inlines = [MarkerInline]


class MapaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # automatically make slug from name


class PropertyAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'as_filter', 'icon_tag', 'status', 'order')
    prepopulated_fields = {'slug': ('name',)}  # automatically make slug from name
    model = Property


class MarkerStatusFilter(SimpleListFilter):
    title = _(u"all statuses")
    parameter_name = u"statuses"

    def lookups(self, request, model_admin):
        return ((None, _(u"Visible")),
                ('all', _('All')),
                ("unvisible", _(u"Invisible")))

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
            return queryset.filter(Q(status__show_to_mapper=True) & Q(layer__status__show_to_mapper=True))
        if self.value() == "unvisible":
            return queryset.exclude(Q(status__show_to_mapper=True) & Q(layer__status__show_to_mapper=True))


class MarkerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'desc', 'layer', 'minzoom', 'status', 'default_icon_image', 'id', 'poi_count', 'created_at', 'last_modification')
    list_filter = (MarkerStatusFilter, 'layer', 'status',)
    search_fields = ('name', 'desc',)
    readonly_fields = ('poi_count', 'created_at', 'last_modification', )
    prepopulated_fields = {'slug': ('name',)}

    def default_icon_image(self, obj):
        if obj.default_icon:
            return '<img src="%s"/>' % obj.default_icon.url
    default_icon_image.short_description = _("icon")
    default_icon_image.allow_tags = True

    def has_change_permission(self, request, obj=None):
        if obj is None and request.user.has_perm(u'webmap.can_only_view'):
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


class MapPresetAdmin(SortableAdminMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'base_layer', 'order')
    filter_horizontal = ('overlay_layers',)


class LegendAdmin(admin.ModelAdmin):
    form = LegendAdminForm
    list_display = ('name', 'image_tag', 'desc',)
    prepopulated_fields = {'slug': ('name',)}


class PhotoAdmin(ImportExportModelAdmin, admin. ModelAdmin):
    form = PhotoAdminForm
    list_display = ('id', 'name', 'poi', 'image_tag', 'author', 'photographer', 'created_at', 'last_modification', 'order', 'license', 'desc', 'photo')
    readonly_fields = ('author', 'updated_by', 'created_at', 'last_modification')
    search_fields = ('name', 'poi__name', )
    raw_id_fields = ('poi', )
    list_filter = ('license', 'status', SectorFilter, 'author', 'poi__properties')
    list_per_page = 20

    def has_change_permission(self, request, obj=None):
        if request.user.has_perm(u'webmap.can_view_photo_list'):
            return super(PhotoAdmin, self).has_change_permission(request, obj)
        return False

    def has_add_permission(self, request):
        if request.user.has_perm(u'webmap.can_view_photo_list'):
            return super(PhotoAdmin, self).has_add_permission(request)
        return False


class BaseLayerAdmin(SortableAdminMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'url', 'order')
    prepopulated_fields = {'slug': ('name',)}  # automatically make slug from name

admin.site.register(Poi, PoiAdmin)
admin.site.register(OverlayLayer, OverlayLayerAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Marker, MarkerAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Legend, LegendAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(BaseLayer, BaseLayerAdmin)
admin.site.register(MapPreset, MapPresetAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
