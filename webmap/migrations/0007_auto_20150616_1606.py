# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0006_auto_20150607_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappreset',
            name='overlay_layers',
            field=models.ManyToManyField(to='webmap.OverlayLayer', verbose_name='overlay layers', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='poi',
            name='properties',
            field=models.ManyToManyField(help_text='POI properties', to='webmap.Property', verbose_name='properties', blank=True),
            preserve_default=True,
        ),
    ]
