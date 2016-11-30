# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-30 17:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0014_auto_20160626_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='legend',
            name='en_name',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='English name'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photo_create', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photo_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
        ),
        migrations.AlterField(
            model_name='poi',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poi_create', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='poi',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poi_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
        ),
    ]
