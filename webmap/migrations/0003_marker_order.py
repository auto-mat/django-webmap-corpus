# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def init_order(apps, schema_editor):
    Marker = apps.get_model("webmap", "Marker")
    for i, marker in enumerate(Marker.objects.all()):
        marker.order = i
        marker.save()


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0002_layer_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='order',
            field=models.IntegerField(default=0, verbose_name='order'),
            preserve_default=True,
        ),
        migrations.RunPython(init_order),
    ]
