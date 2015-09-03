# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0008_mappreset_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappreset',
            name='desc',
            field=models.TextField(help_text='Map preset description.', null=True, verbose_name='description', blank=True),
        ),
    ]
