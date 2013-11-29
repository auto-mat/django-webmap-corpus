# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Status'
        db.create_table(u'django_webmap_corpus_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('show', self.gf('django.db.models.fields.BooleanField')()),
            ('show_to_mapper', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'django_webmap_corpus', ['Status'])

        # Adding model 'Layer'
        db.create_table(u'django_webmap_corpus_layer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_webmap_corpus.Status'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'django_webmap_corpus', ['Layer'])

        # Adding model 'Marker'
        db.create_table(u'django_webmap_corpus_marker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('layer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_webmap_corpus.Layer'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_webmap_corpus.Status'])),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('default_icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('minzoom', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('maxzoom', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
            ('line_width', self.gf('django.db.models.fields.FloatField')(default=2)),
            ('line_color', self.gf('colorful.fields.RGBColorField')(default='#ffc90e', max_length=7)),
        ))
        db.send_create_signal(u'django_webmap_corpus', ['Marker'])

        # Adding model 'Sector'
        db.create_table(u'django_webmap_corpus_sector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
        ))
        db.send_create_signal(u'django_webmap_corpus', ['Sector'])

        # Adding model 'Poi'
        db.create_table(u'django_webmap_corpus_poi', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('marker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pois', to=orm['django_webmap_corpus.Marker'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['django_webmap_corpus.Status'])),
            ('importance', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_extra', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('properties_cache', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modification', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='poi_create', null=True, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='poi_update', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'django_webmap_corpus', ['Poi'])

        # Adding M2M table for field properties on 'Poi'
        m2m_table_name = db.shorten_name(u'django_webmap_corpus_poi_properties')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poi', models.ForeignKey(orm[u'django_webmap_corpus.poi'], null=False)),
            ('property', models.ForeignKey(orm[u'django_webmap_corpus.property'], null=False))
        ))
        db.create_unique(m2m_table_name, ['poi_id', 'property_id'])

        # Adding model 'Property'
        db.create_table(u'django_webmap_corpus_property', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_webmap_corpus.Status'])),
            ('as_filter', self.gf('django.db.models.fields.BooleanField')()),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('default_icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'django_webmap_corpus', ['Property'])

        # Adding model 'License'
        db.create_table(u'django_webmap_corpus_license', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'django_webmap_corpus', ['License'])

        # Adding model 'Photo'
        db.create_table(u'django_webmap_corpus_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poi', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photos', to=orm['django_webmap_corpus.Poi'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('licence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_webmap_corpus.License'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photo_create', null=True, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photo_update', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'django_webmap_corpus', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Status'
        db.delete_table(u'django_webmap_corpus_status')

        # Deleting model 'Layer'
        db.delete_table(u'django_webmap_corpus_layer')

        # Deleting model 'Marker'
        db.delete_table(u'django_webmap_corpus_marker')

        # Deleting model 'Sector'
        db.delete_table(u'django_webmap_corpus_sector')

        # Deleting model 'Poi'
        db.delete_table(u'django_webmap_corpus_poi')

        # Removing M2M table for field properties on 'Poi'
        db.delete_table(db.shorten_name(u'django_webmap_corpus_poi_properties'))

        # Deleting model 'Property'
        db.delete_table(u'django_webmap_corpus_property')

        # Deleting model 'License'
        db.delete_table(u'django_webmap_corpus_license')

        # Deleting model 'Photo'
        db.delete_table(u'django_webmap_corpus_photo')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_webmap_corpus.layer': {
            'Meta': {'ordering': "['order']", 'object_name': 'Layer'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_webmap_corpus.Status']"})
        },
        u'django_webmap_corpus.license': {
            'Meta': {'object_name': 'License'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'django_webmap_corpus.marker': {
            'Meta': {'ordering': "['-layer__order', 'name']", 'object_name': 'Marker'},
            'default_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_webmap_corpus.Layer']"}),
            'line_color': ('colorful.fields.RGBColorField', [], {'default': "'#ffc90e'", 'max_length': '7'}),
            'line_width': ('django.db.models.fields.FloatField', [], {'default': '2'}),
            'maxzoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'minzoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_webmap_corpus.Status']"})
        },
        u'django_webmap_corpus.photo': {
            'Meta': {'object_name': 'Photo'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_create'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_webmap_corpus.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'poi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': u"orm['django_webmap_corpus.Poi']"}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_update'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'django_webmap_corpus.poi': {
            'Meta': {'object_name': 'Poi'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'poi_create'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importance': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'last_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'marker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pois'", 'to': u"orm['django_webmap_corpus.Marker']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'properties': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['django_webmap_corpus.Property']", 'null': 'True', 'blank': 'True'}),
            'properties_cache': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'to': u"orm['django_webmap_corpus.Status']"}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'poi_update'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'django_webmap_corpus.property': {
            'Meta': {'ordering': "['order']", 'object_name': 'Property'},
            'as_filter': ('django.db.models.fields.BooleanField', [], {}),
            'default_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_webmap_corpus.Status']"})
        },
        u'django_webmap_corpus.sector': {
            'Meta': {'object_name': 'Sector'},
            'geom': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'django_webmap_corpus.status': {
            'Meta': {'object_name': 'Status'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'show': ('django.db.models.fields.BooleanField', [], {}),
            'show_to_mapper': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['django_webmap_corpus']