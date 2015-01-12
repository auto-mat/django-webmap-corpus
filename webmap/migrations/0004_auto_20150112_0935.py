# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webmap.utils


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0003_marker_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapPreset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of preset', max_length=255, verbose_name='name')),
                ('icon', models.ImageField(upload_to=b'preset_icons', storage=webmap.utils.SlugifyFileSystemStorage(), verbose_name='preset icon')),
                ('base_layer', models.ForeignKey(verbose_name='base_layer', to='webmap.BaseLayer')),
                ('overlay_layers', models.ManyToManyField(to='webmap.OverlayLayer', null=True, verbose_name='overlay layers', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='marker',
            options={'ordering': ['order'], 'verbose_name': 'marker', 'verbose_name_plural': 'markers', 'permissions': [('can_only_view', 'Can only view')]},
        ),
    ]
