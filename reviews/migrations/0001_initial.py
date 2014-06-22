# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Review'
        db.create_table(u'reviews_review', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quests.Quests'])),
            ('reviewed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.QuestrUserProfile'])),
            ('rating_1', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=5, decimal_places=2)),
            ('rating_2', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=5, decimal_places=2)),
            ('rating_3', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=5, decimal_places=2)),
            ('rating_4', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=5, decimal_places=2)),
            ('final_rating', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=5, decimal_places=2)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(default=None)),
        ))
        db.send_create_signal(u'reviews', ['Review'])


    def backwards(self, orm):
        # Deleting model 'Review'
        db.delete_table(u'reviews_review')


    models = {
        u'quests.quests': {
            'Meta': {'object_name': 'Quests'},
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'delivery_code': ('django.db.models.fields.TextField', [], {'default': "'121212'"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'dstaddress': ('django.db.models.fields.TextField', [], {}),
            'dstcity': ('django.db.models.fields.TextField', [], {'default': "'Toronto'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isaccepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isnotified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_images': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'questrs': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.QuestrUserProfile']"}),
            'reward': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '2'}),
            'shipper': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.TextField', [], {'default': "'backpack'"}),
            'srcaddress': ('django.db.models.fields.TextField', [], {}),
            'srccity': ('django.db.models.fields.TextField', [], {'default': "'Toronto'"}),
            'status': ('django.db.models.fields.TextField', [], {'default': "'new'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reviews.review': {
            'Meta': {'object_name': 'Review'},
            'description': ('django.db.models.fields.TextField', [], {'default': 'None'}),
            'final_rating': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '5', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quests.Quests']"}),
            'rating_1': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '5', 'decimal_places': '2'}),
            'rating_2': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '5', 'decimal_places': '2'}),
            'rating_3': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '5', 'decimal_places': '2'}),
            'rating_4': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '5', 'decimal_places': '2'}),
            'reviewed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.QuestrUserProfile']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'users.questruserprofile': {
            'Meta': {'object_name': 'QuestrUserProfile'},
            'account_status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1', 'blank': 'True'}),
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
            'is_shipper': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['reviews']