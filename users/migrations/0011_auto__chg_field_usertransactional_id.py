# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'UserTransactional.id'
        # db.alter_column(u'users_usertransactional', u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))
        db.execute("CREATE SEQUENCE users_usertransactional_id_seq")
        db.execute("SELECT setval('users_usertransactional_id_seq', (SELECT MAX(id) FROM users_usertransactional))")
        db.execute("ALTER TABLE users_usertransactional ALTER COLUMN id SET DEFAULT nextval('users_usertransactional_id_seq'::regclass)")


    def backwards(self, orm):

        # Changing field 'UserTransactional.id'
        # db.alter_column(u'users_usertransactional', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))
        db.execute("ALTER TABLE users_usertransactional ALTER COLUMN id DROP DEFAULT")
        db.execute("DROP SEQUENCE users_usertransactional_id_seq")


    models = {
        u'users.questrtoken': {
            'Meta': {'object_name': 'QuestrToken'},
            'timeframe': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'token_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        u'users.questruserprofile': {
            'Meta': {'object_name': 'QuestrUserProfile'},
            'account_status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1', 'blank': 'True'}),
            'address': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            'avatar_file_name': ('django.db.models.fields.files.ImageField', [], {'max_length': '9999'}),
            'biography': ('django.db.models.fields.TextField', [], {'max_length': '9999', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'displayname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100'}),
            'email_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_shipper': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notificationprefs': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            'notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '5', 'decimal_places': '2'})
        },
        u'users.usertransactional': {
            'Meta': {'object_name': 'UserTransactional'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['users']