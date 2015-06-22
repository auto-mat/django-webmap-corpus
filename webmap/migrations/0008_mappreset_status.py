# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0007_auto_20150616_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappreset',
            name='status',
            field=models.ForeignKey(default=None, verbose_name='status', to='webmap.Status', null=True),
        ),
    ]
