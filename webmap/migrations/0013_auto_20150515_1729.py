# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0012_line_to_multiline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poi',
            name='geom',
        ),
        migrations.RenameField(
            model_name='poi',
            old_name='geom_multi',
            new_name='geom',
        ),
    ]
