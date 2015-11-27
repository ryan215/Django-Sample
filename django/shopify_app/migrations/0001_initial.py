# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShopifySession'
        db.create_table(u'shopify_app_shopifysession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shop_url', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal(u'shopify_app', ['ShopifySession'])


    def backwards(self, orm):
        # Deleting model 'ShopifySession'
        db.delete_table(u'shopify_app_shopifysession')


    models = {
        u'shopify_app.shopifysession': {
            'Meta': {'object_name': 'ShopifySession'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shop_url': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['shopify_app']