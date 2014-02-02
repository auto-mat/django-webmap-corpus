# -*- coding: utf-8 -*-
import fgp
import admin_image_widget

from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db import models
from django.core.cache import cache
from django.forms import ModelForm
from author.decorators import with_author
from positions import PositionField
from constance import config

from colorful.fields import RGBColorField

from .utils import SlugifyFileSystemStorage


class Status(models.Model):
    "Stavy zobrazeni konkretniho objektu, vrstvy apod. - aktivni, navrzeny, zruseny, ..."
    name = models.CharField(unique=True, max_length=255, verbose_name=_(u"name"), help_text=_(u"Status name"))
    desc = models.TextField(null=True, blank=True, verbose_name=_("description"), help_text=_(u"Status description."))
    show = models.BooleanField(help_text=_(u"Show to map user"), verbose_name=_("show"))
    show_to_mapper = models.BooleanField(help_text=_(u"Show to mapper"), verbose_name=_("show to mapper"))

    class Meta:
        verbose_name = _(u"status")
        verbose_name_plural = _("statuses")

    def __unicode__(self):
        return self.name


class Layer(models.Model):
    "Vrstvy, ktere se zobrazi v konkretni mape"
    name = models.CharField(max_length=255, verbose_name=_(u"name"), help_text=_(u"Name of the layer"), default="")
    slug = models.SlugField(unique=True, verbose_name=_(u"name in URL"))
    desc = models.TextField(null=True, blank=True, verbose_name=_("description"), help_text=_("Layer description."))
    status = models.ForeignKey(Status, verbose_name=_("status"))
    order = PositionField(verbose_name=_("order"))
    remark = models.TextField(null=True, blank=True, help_text=_(u"Internal information about layer."), verbose_name=_("internal remark"))
    enabled = models.BooleanField(verbose_name=_(u"Enabled by defalut"), help_text=_(u"True = the layer is enabled on map load"), default=True)

    class Meta:
        verbose_name = _(u"layer")
        verbose_name_plural = _(u"layers")
        ordering = ['order']

    def __unicode__(self):
        return self.name


class OverlayLayer(Layer):
    class Meta:
        verbose_name = _(u"overlay layer")
        verbose_name_plural = _(u"overlay layers")


class Marker(models.Model):
    "Map markers with display style definition."
    name = models.CharField(unique=True, max_length=255, verbose_name=_(u"name"), help_text=_("Name of the marker."))
    slug = models.SlugField(unique=True, verbose_name=_(u"name in URL"), null=True)

    # Relationships
    layer = models.ForeignKey(OverlayLayer, verbose_name=_("layer"))
    status = models.ForeignKey(Status, verbose_name=_("status"))

    # content
    desc = models.TextField(null=True, blank=True, verbose_name=_("description"), help_text=_(u"Detailed marker descrption."))
    remark = models.TextField(null=True, blank=True, help_text=_(u"Internal information about layer."), verbose_name=_("internal remark"))

    # Base icon and zoom dependent display range
    default_icon = models.ImageField(null=True, blank=True, upload_to='icons', storage=SlugifyFileSystemStorage(), verbose_name=_("default icon"))
    menu_icon = models.ImageField(null=True, blank=True, upload_to='icons/marker/menu', storage=SlugifyFileSystemStorage(), verbose_name=_("menu icon"))
    minzoom = models.PositiveIntegerField(default=1, verbose_name=_("Minimal zoom"), help_text=_(u"Minimal zoom in which the POIs of this marker will be shown on the map."))
    maxzoom = models.PositiveIntegerField(default=10, verbose_name=_("Maximal zoom"), help_text=_(u"Maximal zoom in which the POIs of this marker will be shown on the map."))

    # Linear elements style
    line_width = models.FloatField(verbose_name=_(u"line width"), default=2,)
    line_color = RGBColorField(default="#ffc90e", verbose_name=_("line color"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    last_modification = models.DateTimeField(auto_now=True, verbose_name=_("last modification at"))

    def line_color_kml(this):
        color = this.line_color[1:]
        return "88" + color[4:6] + color[2:4] + color[0:2]

    class Meta:
        permissions = [
            ("can_only_view", "Can only view"),
        ]
        verbose_name = _(u"marker")
        verbose_name_plural = _(u"markers")
        ordering = ['-layer__order', 'name']

    def __unicode__(self):
        return self.name


class VisibleManager(models.GeoManager):
    "Manager that will return objects visible on the map"
    def get_query_set(self):
        return super(VisibleManager, self).get_query_set().filter(status__show=True, marker__status__show=True, marker__layer__status__show=True)


class Sector(models.Model):
    "Map sector"
    name = models.CharField(max_length=255, verbose_name=_(u"name"))
    slug = models.SlugField(unique=True, verbose_name=_(u"name in URL"))

    geom = models.PolygonField(verbose_name=_(u"area"), srid=4326, help_text=_(u"Sector area"))
    objects = models.GeoManager()

    class Meta:
        verbose_name = _(u"sector")
        verbose_name_plural = _(u"sectors")


@with_author
@fgp.guard('importance', 'status', name='can_edit_advanced_fields')
class Poi(models.Model):
    "Place in map"
    name = models.CharField(max_length=255, verbose_name=_(u"name"), help_text=_(u"Exact place name"))

    # Relationships
    marker = models.ForeignKey(Marker, limit_choices_to={'status__show_to_mapper': 'True', 'layer__status__show_to_mapper': 'True'}, verbose_name=_(u"marker"), help_text=_("Select icon, that will be shown in map"), related_name="pois")
    status = models.ForeignKey(Status, default=config.DEFAULT_STATUS_ID, help_text=_("POI status, determinse if it will be shown in map"), verbose_name=_(u"status"))
    properties = models.ManyToManyField('Property', blank=True, null=True, help_text=_("POI properties"), verbose_name=_("properties"), limit_choices_to={'status__show_to_mapper': 'True'})

    importance = models.SmallIntegerField(default=0, verbose_name=_(u"importance"),
                 help_text=_(u"""Minimal zoom modificator (use 20+ to show always).<br/>"""))

    # Geographical intepretation
    geom = models.GeometryField(verbose_name=_(u"place geometry"), srid=4326, help_text=_(u"""Add point: Select pencil with plus sign icon and place your point to the map.<br/>
            Add line: Select line icon and by clicking to map draw the line. Finish drawing with double click.<br/>
            Add area: Select area icon and by clicking to mapy draw the area. Finish drawing with double click.<br/>
            Object edition: Select the first icon and then select object in map. Draw points in map to move them, use points in the middle of sections to add new edges."""))
    objects = models.GeoManager()

    # Own content (facultative)

    desc = models.TextField(null=True, blank=True, verbose_name=_(u"description"), help_text=_(u"Text that will be shown after selecting POI."))
    desc_extra = models.TextField(null=True, blank=True, verbose_name=_(u"detailed description"), help_text=_("Text that extends the description."))
    url = models.URLField(null=True, blank=True, verbose_name=_("URL"), help_text=_(u"Link to the web page of the place."))
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_(u"adress"), help_text=_(u"Poi address (street, house number)"))
    remark = models.TextField(null=True, blank=True, verbose_name=_(u"Internal remark"), help_text=_(u"Internal information about POI."))

    # zde se ulozi slugy vsech vlastnosti, aby se pri renederovani kml
    # nemusel delat db dotaz pro kazde Poi na jeho vlastnosti
    properties_cache = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    last_modification = models.DateTimeField(auto_now=True, verbose_name=_("last modification at"))

    visible = VisibleManager()

    class Meta:
        permissions = [
            ("can_only_own_data_only", "Can only edit his own data"),
        ]
        verbose_name = _("place")
        verbose_name_plural = _("places")

    def __unicode__(self):
        return self.name

    def save_properties_cache(self):
        self.properties_cache = u",".join([v.slug for v in self.properties.filter(status__show=True)])
        self.save()

    def get_absolute_url(self):
        return "/misto/%i/" % self.id

    def properties_list(self):
        return u", ".join([p.name for p in self.properties.all()])

from django.db.models.signals import m2m_changed, post_save, post_delete


def update_properties_cache(sender, instance, action, reverse, model, pk_set, **kwargs):
    "Property cache actualization at POI save. It will not work yet after property removal."
    if action == 'post_add':
        instance.save_properties_cache()
m2m_changed.connect(update_properties_cache, Poi.properties.through)


class Legend(models.Model):
    "map legend items of underlay"
    name = models.CharField(unique=True, max_length=255, verbose_name=_(u"name"))
    slug = models.SlugField(unique=True, verbose_name=_(u"name in URL"))
    desc = models.TextField(null=True, blank=True, verbose_name=_(u"description"))
    image = models.ImageField(upload_to='ikony', storage=SlugifyFileSystemStorage(), verbose_name=_(u"image"))

    class Meta:
        verbose_name = _(u"legend item")
        verbose_name_plural = _(u"legend items")

    def __unicode__(self):
        return self.name

    def image_tag(self):
        import admin_image_widget
        return admin_image_widget.list_display(self.image)
    image_tag.allow_tags = True
    image_tag.short_description = _(u"image")


class LegendAdminForm(ModelForm):
    class Meta:
        model = Legend
        widgets = {
            'image': admin_image_widget.AdminImageWidget,
        }


def invalidate_cache(sender, instance, **kwargs):
    if sender in [Status, Layer, Marker, Poi, Property, Legend, Sector]:
        cache.clear()
post_save.connect(invalidate_cache)
post_delete.connect(invalidate_cache)


class Property(models.Model):
    "Place properties"
    name = models.CharField(max_length=255, verbose_name=_(u"name"), help_text=_(u"Status name"))
    status = models.ForeignKey(Status, verbose_name=_("status"))
    as_filter = models.BooleanField(verbose_name=_("as filter?"), help_text=_(u"Show as a filter in right map menu?"))
    order = PositionField(verbose_name=_("order"))
    # content
    slug = models.SlugField(unique=True, verbose_name=_("Name in URL"))
    desc = models.TextField(null=True, blank=True, verbose_name=_("description"), help_text=_(u"Property description."))
    remark = models.TextField(null=True, blank=True, verbose_name=_(u"Internal remark"), help_text=_(u"Internal information about the property."))
    default_icon = models.ImageField(null=True, blank=True, upload_to='icons', storage=SlugifyFileSystemStorage(), verbose_name=_("default icon"))

    class Meta:
        verbose_name = _(u"property")
        verbose_name_plural = _(u"properties")
    ordering = ['order']

    def __unicode__(self):
        return self.name

    def icon_tag(self):
        import admin_image_widget
        return admin_image_widget.list_display(self.default_icon)
    icon_tag.allow_tags = True
    icon_tag.short_description = _(u"icon")


class License(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u"name"), help_text=_(u"License name"))
    desc = models.TextField(null=True, blank=True, verbose_name=_("description"), help_text=_(u"License description."))

    class Meta:
        verbose_name = _(u"license")
        verbose_name_plural = _(u"licenses")

    def __unicode__(self):
        return self.name


class BaseLayer(Layer):
    url = models.URLField(null=True, blank=True, verbose_name=_("URL"), help_text=_(u"Base layer tiles url. e.g. "))

    class Meta:
        verbose_name = _(u"base layer")
        verbose_name_plural = _(u"base layers")

    def __unicode__(self):
        return self.name


@with_author
class Photo(models.Model):
    poi = models.ForeignKey(Poi, related_name="photos", verbose_name=_("poi"))
    name = models.CharField(max_length=255, verbose_name=_(u"name"), help_text=_(u"Photo name"))
    desc = models.TextField(null=True, blank=True, verbose_name=_("description"), help_text=_(u"Photo description."))
    license = models.ForeignKey(License, verbose_name=_("license"))
    order = PositionField(verbose_name=_("order"), collection="poi")
    photographer = models.CharField(max_length=255, verbose_name=_(u"Photography author"), blank=True, help_text=_(u"Full name of the author of the photography"))

    photo = models.ImageField(null=False, blank=False,
        upload_to='photo', storage=SlugifyFileSystemStorage(),
        verbose_name=_(u"photo"),
        help_text=_(u"Upload photo in full resolution."),
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_("created at"))
    last_modification = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_("last modification at"))

    def image_tag(self):
        import admin_image_widget
        return admin_image_widget.list_display(self.photo)
    image_tag.short_description = _(u"image")
    image_tag.allow_tags = True

    class Meta:
        verbose_name = _(u"photo")
        verbose_name_plural = _(u"photographies")

    ordering = ['order']


class PhotoAdminForm(ModelForm):
    class Meta:
        model = Photo
        widgets = {
            'photo': admin_image_widget.AdminImageWidget,
        }
