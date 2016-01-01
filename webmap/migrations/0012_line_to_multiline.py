# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.gis.geos import GeometryCollection

def change_line_to_multiline(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Poi  = apps.get_model("webmap", "Poi")
    for poi in Poi.objects.all():
        if poi.geom:
            poi.geom_multi = GeometryCollection([poi.geom, ])
            poi.save()

class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0011_auto_20160101_0521'),
    ]

    operations = [
        migrations.RunPython(change_line_to_multiline),
    ]
