# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def make_order(apps, schema_editor):
   # We can't import the Person model directly as it may be a newer
   # version than this migration expects. We use the historical version.
   MapPreset  = apps.get_model("webmap", "MapPreset")
   for i, preset in enumerate(MapPreset.objects.all()):
      preset.order = i
      preset.save()

class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0005_auto_20150607_1533'),
    ]

    operations = [
          migrations.RunPython(make_order),
    ]
