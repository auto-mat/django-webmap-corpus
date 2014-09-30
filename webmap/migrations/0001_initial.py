# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields
import django.contrib.gis.db.models.fields
from django.conf import settings
import webmap.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', help_text='Name of the layer', max_length=255, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='name in URL')),
                ('desc', models.TextField(help_text='Layer description.', null=True, verbose_name='description', blank=True)),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('remark', models.TextField(help_text='Internal information about layer.', null=True, verbose_name='internal remark', blank=True)),
                ('enabled', models.BooleanField(default=True, help_text='True = the layer is enabled on map load', verbose_name='Enabled by defalut')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'layer',
                'verbose_name_plural': 'layers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BaseLayer',
            fields=[
                ('layer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='webmap.Layer')),
                ('url', models.URLField(help_text='Base layer tiles url. e.g. ', null=True, verbose_name='URL', blank=True)),
            ],
            options={
                'verbose_name': 'base layer',
                'verbose_name_plural': 'base layers',
            },
            bases=('webmap.layer',),
        ),
        migrations.CreateModel(
            name='Legend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='name in URL')),
                ('desc', models.TextField(null=True, verbose_name='description', blank=True)),
                ('image', models.ImageField(upload_to=b'ikony', storage=webmap.utils.SlugifyFileSystemStorage(), verbose_name='image')),
            ],
            options={
                'verbose_name': 'legend item',
                'verbose_name_plural': 'legend items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='License name', max_length=255, verbose_name='name')),
                ('desc', models.TextField(help_text='License description.', null=True, verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'license',
                'verbose_name_plural': 'licenses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of the marker.', unique=True, max_length=255, verbose_name='name')),
                ('slug', models.SlugField(unique=True, null=True, verbose_name='name in URL')),
                ('desc', models.TextField(help_text='Detailed marker descrption.', null=True, verbose_name='description', blank=True)),
                ('remark', models.TextField(help_text='Internal information about layer.', null=True, verbose_name='internal remark', blank=True)),
                ('default_icon', models.ImageField(storage=webmap.utils.SlugifyFileSystemStorage(), upload_to=b'icons', null=True, verbose_name='default icon', blank=True)),
                ('menu_icon', models.ImageField(storage=webmap.utils.SlugifyFileSystemStorage(), upload_to=b'icons/marker/menu', null=True, verbose_name='menu icon', blank=True)),
                ('minzoom', models.PositiveIntegerField(default=1, help_text='Minimal zoom in which the POIs of this marker will be shown on the map.', verbose_name='Minimal zoom')),
                ('maxzoom', models.PositiveIntegerField(default=10, help_text='Maximal zoom in which the POIs of this marker will be shown on the map.', verbose_name='Maximal zoom')),
                ('line_width', models.FloatField(default=2, verbose_name='line width')),
                ('line_color', colorful.fields.RGBColorField(default=b'#ffc90e', verbose_name='line color')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='last modification at')),
            ],
            options={
                'ordering': ['-layer__order', 'name'],
                'verbose_name': 'marker',
                'verbose_name_plural': 'markers',
                'permissions': [('can_only_view', 'Can only view')],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OverlayLayer',
            fields=[
                ('layer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='webmap.Layer')),
            ],
            options={
                'verbose_name': 'overlay layer',
                'verbose_name_plural': 'overlay layers',
            },
            bases=('webmap.layer',),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Photo name', max_length=255, verbose_name='name', blank=True)),
                ('desc', models.TextField(help_text='Photo description.', null=True, verbose_name='description', blank=True)),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('photographer', models.CharField(help_text='Full name of the author of the photography', max_length=255, verbose_name='Photography author', blank=True)),
                ('photo', models.ImageField(help_text='Upload photo in full resolution.', upload_to=b'photo', storage=webmap.utils.SlugifyFileSystemStorage(), verbose_name='photo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at', null=True)),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='last modification at', null=True)),
                ('author', models.ForeignKey(related_name=b'photo_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('license', models.ForeignKey(verbose_name='license', to='webmap.License')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'photo',
                'verbose_name_plural': 'photographies',
                'permissions': [('can_view_photo_list', 'Can view photo list')],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Exact place name', max_length=255, verbose_name='name')),
                ('importance', models.SmallIntegerField(default=0, help_text='Minimal zoom modificator (use 20+ to show always).<br/>', verbose_name='importance')),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(help_text='Add point: Select pencil with plus sign icon and place your point to the map.<br/>\n            Add line: Select line icon and by clicking to map draw the line. Finish drawing with double click.<br/>\n            Add area: Select area icon and by clicking to mapy draw the area. Finish drawing with double click.<br/>\n            Object edition: Select the first icon and then select object in map. Draw points in map to move them, use points in the middle of sections to add new edges.', srid=4326, verbose_name='place geometry')),
                ('desc', models.TextField(help_text='Text that will be shown after selecting POI.', null=True, verbose_name='description', blank=True)),
                ('desc_extra', models.TextField(help_text='Text that extends the description.', null=True, verbose_name='detailed description', blank=True)),
                ('url', models.URLField(help_text='Link to the web page of the place.', null=True, verbose_name='URL', blank=True)),
                ('address', models.CharField(help_text='Poi address (street, house number)', max_length=255, null=True, verbose_name='adress', blank=True)),
                ('remark', models.TextField(help_text='Internal information about POI.', null=True, verbose_name='Internal remark', blank=True)),
                ('properties_cache', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='last modification at')),
                ('author', models.ForeignKey(related_name=b'poi_create', verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('marker', models.ForeignKey(related_name=b'pois', verbose_name='marker', to='webmap.Marker', help_text='Select icon, that will be shown in map')),
            ],
            options={
                'verbose_name': 'place',
                'verbose_name_plural': 'places',
                'permissions': [('can_only_own_data_only', 'Can only edit his own data'), ('can_edit_advanced_fields', 'Can edit importance status')],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Status name', max_length=255, verbose_name='name')),
                ('as_filter', models.BooleanField(default=False, help_text='Show as a filter in right map menu?', verbose_name='as filter?')),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('slug', models.SlugField(unique=True, verbose_name='Name in URL')),
                ('desc', models.TextField(help_text='Property description.', null=True, verbose_name='description', blank=True)),
                ('remark', models.TextField(help_text='Internal information about the property.', null=True, verbose_name='Internal remark', blank=True)),
                ('default_icon', models.ImageField(storage=webmap.utils.SlugifyFileSystemStorage(), upload_to=b'icons', null=True, verbose_name='default icon', blank=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'property',
                'verbose_name_plural': 'properties',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='name in URL')),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(help_text='Sector area', srid=4326, verbose_name='area')),
            ],
            options={
                'verbose_name': 'sector',
                'verbose_name_plural': 'sectors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Status name', unique=True, max_length=255, verbose_name='name')),
                ('desc', models.TextField(help_text='Status description.', null=True, verbose_name='description', blank=True)),
                ('show', models.BooleanField(default=False, help_text='Show to map user', verbose_name='show')),
                ('show_to_mapper', models.BooleanField(default=False, help_text='Show to mapper', verbose_name='show to mapper')),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statuses',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='property',
            name='status',
            field=models.ForeignKey(verbose_name='status', to='webmap.Status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poi',
            name='properties',
            field=models.ManyToManyField(help_text='POI properties', to='webmap.Property', null=True, verbose_name='properties', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poi',
            name='status',
            field=models.ForeignKey(default=0, verbose_name='status', to='webmap.Status', help_text='POI status, determinse if it will be shown in map'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poi',
            name='updated_by',
            field=models.ForeignKey(related_name=b'poi_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='poi',
            field=models.ForeignKey(related_name=b'photos', verbose_name='poi', to='webmap.Poi'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='updated_by',
            field=models.ForeignKey(related_name=b'photo_update', verbose_name='last updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='marker',
            name='layer',
            field=models.ForeignKey(verbose_name='layer', to='webmap.Layer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='marker',
            name='status',
            field=models.ForeignKey(verbose_name='status', to='webmap.Status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='layer',
            name='status',
            field=models.ForeignKey(verbose_name='status', to='webmap.Status'),
            preserve_default=True,
        ),
    ]
