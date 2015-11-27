# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ShopifySession.access_token'
        db.alter_column(u'shopify_app_shopifysession', 'access_token', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'ShopifySession.shop_url'
        db.alter_column(u'shopify_app_shopifysession', 'shop_url', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):

        # Changing field 'ShopifySession.access_token'
        db.alter_column(u'shopify_app_shopifysession', 'access_token', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'ShopifySession.shop_url'
        db.alter_column(u'shopify_app_shopifysession', 'shop_url', self.gf('django.db.models.fields.CharField')(max_length=30))

    models = {
        u'shopify_app.shopifysession': {
            'Meta': {'object_name': 'ShopifySession'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shop_url': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['shopify_app']