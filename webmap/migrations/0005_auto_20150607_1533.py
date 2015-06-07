# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0004_auto_20150112_0935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mappreset',
            options={'ordering': ['order'], 'verbose_name': 'map preset', 'verbose_name_plural': 'map presets'},
        ),
        migrations.AddField(
            model_name='mappreset',
            name='order',
            field=models.IntegerField(default=0, verbose_name='order'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mappreset',
            name='base_layer',
            field=models.ForeignKey(verbose_name='base layer', to='webmap.BaseLayer'),
            preserve_default=True,
        ),
    ]
