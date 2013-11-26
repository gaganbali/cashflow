# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RecurringAdjustments'
        db.create_table('main_recurringadjustments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('begin_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('date_offset', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('exact', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('main', ['RecurringAdjustments'])

        # Adding model 'RecurItemRaw'
        db.create_table('main_recuritemraw', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('exp_inc', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('freq_num', self.gf('django.db.models.fields.IntegerField')()),
            ('freq_interval', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('begin_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['RecurItemRaw'])

        # Adding model 'OverrideItem'
        db.create_table('main_overrideitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recur_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.RecurItemRaw'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['OverrideItem'])


    def backwards(self, orm):
        # Deleting model 'RecurringAdjustments'
        db.delete_table('main_recurringadjustments')

        # Deleting model 'RecurItemRaw'
        db.delete_table('main_recuritemraw')

        # Deleting model 'OverrideItem'
        db.delete_table('main_overrideitem')


    models = {
        'main.overrideitem': {
            'Meta': {'object_name': 'OverrideItem'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recur_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.RecurItemRaw']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'main.recuritemraw': {
            'Meta': {'object_name': 'RecurItemRaw'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'exp_inc': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'freq_interval': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'freq_num': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'main.recurringadjustments': {
            'Meta': {'object_name': 'RecurringAdjustments'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'date_offset': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'exact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['main']