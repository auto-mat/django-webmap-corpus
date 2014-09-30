# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webmap.utils


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='icon',
            field=models.ImageField(storage=webmap.utils.SlugifyFileSystemStorage(), upload_to=b'layer_icons', null=True, verbose_name='layer icon', blank=True),
            preserve_default=True,
        ),
    ]
