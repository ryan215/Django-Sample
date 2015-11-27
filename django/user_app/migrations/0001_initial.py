# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomUser'
        db.create_table(u'user_app_customuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=50, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('tier', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('lat', self.gf('django.db.models.fields.CharField')(default='29.760193', max_length=30, blank=True)),
            ('lng', self.gf('django.db.models.fields.CharField')(default='-95.369390', max_length=30, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('instagram', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('youtube', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('linkedin', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('plus', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(default='default-profile.svg', max_length=100, blank=True)),
            ('bio', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('referred_by', self.gf('django.db.models.fields.related.ForeignKey')(default=2, related_name='user_reference', null=True, blank=True, to=orm['user_app.Professional'])),
            ('shopify_id', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('chargify_id', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('stripe_id', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('profile_img_id', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('connection', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_connections', null=True, to=orm['user_app.Professional'])),
            ('primary_address', self.gf('django.db.models.fields.related.OneToOneField')(related_name='owner', null=True, on_delete=models.SET_NULL, to=orm['user_app.Address'], blank=True, unique=True)),
            ('is_professional', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_upgraded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'user_app', ['CustomUser'])

        # Adding M2M table for field groups on 'CustomUser'
        m2m_table_name = db.shorten_name(u'user_app_customuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customuser', models.ForeignKey(orm[u'user_app.customuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['customuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'CustomUser'
        m2m_table_name = db.shorten_name(u'user_app_customuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customuser', models.ForeignKey(orm[u'user_app.customuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['customuser_id', 'permission_id'])

        # Adding model 'Address'
        db.create_table(u'user_app_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('corporation', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('street_line1', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('street_line2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('postal_box', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='US', max_length=100, blank=True)),
            ('lat', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('lng', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal(u'user_app', ['Address'])

        # Adding model 'UniqueLocation'
        db.create_table(u'user_app_uniquelocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('counter', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'user_app', ['UniqueLocation'])

        # Adding model 'Certification'
        db.create_table(u'user_app_certification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='certifications', null=True, to=orm['user_app.CustomUser'])),
            ('certification_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('certification_number', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'user_app', ['Certification'])

        # Adding model 'Professional'
        db.create_table(u'user_app_professional', (
            (u'customuser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['user_app.CustomUser'], unique=True, primary_key=True)),
            ('profession', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_accepting', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('queue', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fitness_sales_experience', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('education', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('group_fitness_experience', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('nutritionist_experience', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('certified_nutritionist', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('certified_group_fitness', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('certification_name1', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('certification_number1', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('certification_name2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('certification_number2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'user_app', ['Professional'])


    def backwards(self, orm):
        # Deleting model 'CustomUser'
        db.delete_table(u'user_app_customuser')

        # Removing M2M table for field groups on 'CustomUser'
        db.delete_table(db.shorten_name(u'user_app_customuser_groups'))

        # Removing M2M table for field user_permissions on 'CustomUser'
        db.delete_table(db.shorten_name(u'user_app_customuser_user_permissions'))

        # Deleting model 'Address'
        db.delete_table(u'user_app_address')

        # Deleting model 'UniqueLocation'
        db.delete_table(u'user_app_uniquelocation')

        # Deleting model 'Certification'
        db.delete_table(u'user_app_certification')

        # Deleting model 'Professional'
        db.delete_table(u'user_app_professional')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'user_app.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'corporation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'US'", 'max_length': '100', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'lng': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'postal_box': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'street_line1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'street_line2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        },
        u'user_app.certification': {
            'Meta': {'object_name': 'Certification'},
            'certification_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'certification_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'certifications'", 'null': 'True', 'to': u"orm['user_app.CustomUser']"})
        },
        u'user_app.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_connections'", 'null': 'True', 'to': u"orm['user_app.Professional']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'default': "'default-profile.svg'", 'max_length': '100', 'blank': 'True'}),
            'instagram': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_professional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_upgraded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'lat': ('django.db.models.fields.CharField', [], {'default': "'29.760193'", 'max_length': '30', 'blank': 'True'}),
            'linkedin': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'lng': ('django.db.models.fields.CharField', [], {'default': "'-95.369390'", 'max_length': '30', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'plus': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'primary_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'owner'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['user_app.Address']", 'blank': 'True', 'unique': 'True'}),
            'profile_img_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'referred_by': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'related_name': "'user_reference'", 'null': 'True', 'blank': 'True', 'to': u"orm['user_app.Professional']"}),
            'shopify_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'tier': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'youtube': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'user_app.professional': {
            'Meta': {'object_name': 'Professional', '_ormbases': [u'user_app.CustomUser']},
            'certification_name1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'certification_name2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'certification_number1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'certification_number2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'certified_group_fitness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'certified_nutritionist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'customuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['user_app.CustomUser']", 'unique': 'True', 'primary_key': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'fitness_sales_experience': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'group_fitness_experience': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'is_accepting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nutritionist_experience': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'queue': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'user_app.uniquelocation': {
            'Meta': {'object_name': 'UniqueLocation'},
            'counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['user_app']