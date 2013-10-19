# -*- coding: utf-8 -*-
import datetime
import fgp

from django.contrib.gis.db import models
from django.utils.safestring import mark_safe
from django.core.cache import cache

from django.contrib.auth.models import User
from colorful.fields import RGBColorField

from .utils import SlugifyFileSystemStorage

class Status(models.Model):
    "Stavy zobrazeni konkretniho objektu, vrstvy apod. - aktivni, navrzeny, zruseny, ..."
    name    = models.CharField(unique=True, max_length=255, help_text=u"Název statutu")
    desc    = models.TextField(null=True, blank=True, help_text=u"Popis")
    show    = models.BooleanField(help_text=u"Zobrazit uživateli zvenčí")
    show_to_mapper = models.BooleanField(help_text=u"Zobrazit editorovi mapy")

    class Meta:
        verbose_name_plural = "statuty"
    def __unicode__(self):
        return self.name

class Layer(models.Model):
    "Vrstvy, ktere se zobrazi v konkretni mape"
    name    = models.CharField(max_length=255)                      # Name of the layer
    slug    = models.SlugField(unique=True, verbose_name=u"název v URL")  # Vrstva v URL
    desc    = models.TextField(null=True, blank=True)               # Description
    status  = models.ForeignKey(Status)              # zobrazovaci status
    order   = models.PositiveIntegerField()
    remark  = models.TextField(null=True, blank=True, help_text=u"interni informace o objektu, ktere se nebudou zobrazovat")

    class Meta:
        verbose_name_plural = u"vrstvy"
        ordering = ['order']
    def __unicode__(self):
        return self.name

class Marker(models.Model):
    "Mapove znacky vcetne definice zobrazeni"
    name    = models.CharField(unique=True, max_length=255)   # Name of the mark
    
    # Relationships
    layer  = models.ForeignKey(Layer)              # Kazda znacka lezi prave v jedne vrstve
    status  = models.ForeignKey(Status)              # kvuli vypinani
    
    # icon: Neni zde, ale v tabulce znacky a vztahuje se k rozlicnym zobrazenim 
    # Pro zjednoduseni mame image "default_icon", ale to je jen nouzove reseni, 
    # ktere nesmi nahradit system znacek zavislych na zobrazeni, etc.
    
    # content 
    desc    = models.TextField(null=True, blank=True, help_text=u"podrobny popis znacky")
    remark  = models.TextField(null=True, blank=True, help_text=u"interni informace o objektu, ktere se nebudou zobrazovat")
    
    # Base icon and zoom dependent display range
    default_icon = models.ImageField(null=True, blank=True, upload_to='ikony', storage=SlugifyFileSystemStorage())
    minzoom = models.PositiveIntegerField(default=1)
    maxzoom = models.PositiveIntegerField(default=10)

    # Linear elements style
    line_width = models.FloatField( verbose_name=u"šířka čáry", default=2,)
    line_color = RGBColorField(default="#ffc90e")
    def line_color_kml(this):
        color = this.line_color[1:]
        return "88" + color[4:6] + color[2:4] + color[0:2]

    url     = models.URLField(null=True, blank=True, help_text=u"ukáže se u všech míst s touto značkou, pokud nemají vlastní url")
    
    class Meta:
        permissions = [
            ("can_only_view", "Can only view"),
        ]
        verbose_name_plural = "značky"
        ordering = ['-layer__order', 'name']

    def __unicode__(self):
        return self.name

class VisiblePoiManager(models.GeoManager):
    "Pomocny manazer pro dotazy na Poi se zobrazitelnym statuem"
    def get_query_set(self):
        return super(VisiblePoiManager, self).get_query_set().filter(status__show=True, znacka__status__show=True)

class Sector(models.Model):
    "Sektor mapy"
    name    = models.CharField(max_length=255)
    slug    = models.SlugField(unique=True, verbose_name="Slug")
    
    geom    = models.PolygonField(verbose_name=u"plocha",srid=4326, help_text=u"Plocha sektoru")
    objects = models.GeoManager()

    class Meta:
        verbose_name_plural = u"sektory"

@fgp.guard('dulezitost', 'status', name='can_edit_advanced_fields')
class Poi(models.Model):
    "Misto - bod v mape"
    author = models.ForeignKey(User, verbose_name="Autor")

    name   = models.CharField(max_length=255, verbose_name=u"název", help_text=u"Přesný název místa.")
    
    # Relationships
    marker  = models.ForeignKey(Marker, limit_choices_to = {'status__show_to_mapper': 'True', 'layer__status__show_to_mapper': 'True'}, verbose_name=u"značka", help_text="Zde vyberte ikonu, která se zobrazí na mapě.", related_name="pois")
    status  = models.ForeignKey(Status, default=2, help_text="Status místa; určuje, kde všude se místo zobrazí.")
    properties = models.ManyToManyField('Property', blank=True, null=True, help_text="Určete, jaké má místo vlastnosti. Postupujte podle manuálu.<br/>")
    
    # "dulezitost" - modifikator minimalniho zoomu, ve kterem se misto zobrazuje. 
    dulezitost = models.SmallIntegerField(default=0, verbose_name=u"důležitost",
                 help_text=u"""Modifikátor minimalniho zoomu, ve kterém se místo zobrazuje (20+ bude vidět vždy).<br/>
                               Cíl je mít výběr základních objektů viditelných ve velkých měřítcích
                               a zabránit přetížení mapy značkami v přehledce.<br/>
                               Lze použít pro placenou reklamu! ("Váš podnik bude vidět hned po otevření mapy")""")
    
    # Geographical intepretation
    geom    = models.GeometryField(verbose_name=u"poloha",srid=4326, help_text=u"""Vložení bodu: Klikněte na tužku s plusem a umístěte bod na mapu<br/>
            Kreslení linie: Klikněte na ikonu linie a klikáním do mapy určete lomenou čáru. Kreslení ukončíte dvouklikem.<br/>
            Kreslení oblasti: Klikněte na ikonu oblasti a klikáním do mapy definujte oblast. Kreslení ukončíte dvouklikem.<br/>
            Úprava vložených objektů: Klikněte na první ikonu a potom klikněte na objekt v mapě. Tažením přesouváte body, body uprostřed úseků slouží k vkládání nových bodů do úseku.""")
    objects = models.GeoManager()
    
    # Own content (facultative)

    desc    = models.TextField(null=True, blank=True, verbose_name=u"popis", help_text=u"Text, který se zobrazí na mapě po kliknutí na ikonu.")
    desc_extra = models.TextField(null=True, blank=True, verbose_name=u"podrobný popis", help_text="Text, který rozšiřuje informace výše.")
    url     = models.URLField(null=True, blank=True, help_text=u"Odkaz na webovou stránku místa.")
    remark  = models.TextField(null=True, blank=True, verbose_name=u"interní poznámka", help_text=u"Interní informace o objektu, které se nebudou zobrazovat.")

    # navzdory nazvu jde o fotku v plnem rozliseni
    foto_thumb  = models.ImageField(null=True, blank=True,
                                    upload_to='foto', storage=SlugifyFileSystemStorage(),
                                    verbose_name=u"fotka",
                                    help_text=u"Nahrajte fotku v plné velikosti.",
                                   )
    # zde se ulozi slugy vsech vlastnosti, aby se pri renederovani kml
    # nemusel delat db dotaz pro kazde Poi na jeho vlastnosti
    properties_cache = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Posledni zmena")
    
    viditelne = VisiblePoiManager()
    
    class Meta:
        permissions = [
            ("can_only_own_data_only", "Can only edit his own data"),
        ]
        verbose_name = "místo"
        verbose_name_plural = "místa"
    def __unicode__(self):
        return self.name
    def save_properties_cache(self):
        self.properties_cache = u",".join([v.slug for v in self.properties.filter(status__show=True)])
        self.save()
    def get_absolute_url(self):
        return "/misto/%i/" % self.id

    def save(self, *args, **kwargs):
        self.created_at = datetime.datetime.now()
        super(Poi, self).save(*args, **kwargs)

from django.db.models.signals import m2m_changed, post_save, post_delete
def update_properties_cache(sender, instance, action, reverse, model, pk_set, **kwargs):
    "Aktualizace cache vlastnosti pri ulozeni Poi. Je treba jeste vyresit smazani Vlastnosti"
    if action == 'post_add':
        instance.save_properties_cache()
m2m_changed.connect(update_properties_cache, Poi.properties.through) 

def invalidate_cache(sender, instance, **kwargs):
    if sender in [Status, Layer, Marker, Poi, Property]:
        cache.clear()
post_save.connect(invalidate_cache)
post_delete.connect(invalidate_cache)
    
class Property(models.Model):
    "Vlastnosti mist"
    name    = models.CharField(max_length=255)   # Name of the property
    status  = models.ForeignKey(Status)          # "Statuty"  - tj. active/inactive. Mozny je i boolean "active"
    as_filter  = models.BooleanField()              # Pouzit v levem menu, filtrovat???
    order   = models.PositiveIntegerField()
    # content 
    slug    = models.SlugField(unique=True, verbose_name="Slug")  # Popis tagu v URL
    desc    = models.TextField(null=True, blank=True) # podrobny popis vlastnosti
    remark  = models.TextField(null=True, blank=True, help_text=u"interni informace o objektu, ktere se nebudou zobrazovat")
    default_icon = models.ImageField(null=True, blank=True, upload_to='ikony', storage=SlugifyFileSystemStorage())
   
    class Meta:
        verbose_name_plural = u"properties"
	ordering = ['order']
    def __unicode__(self):
        return self.name
