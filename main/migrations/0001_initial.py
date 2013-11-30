# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RecurItem'
        db.create_table('main_recuritem', (
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, primary_key=True, max_length=30)),
            ('exp_inc', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('freq_num', self.gf('django.db.models.fields.IntegerField')()),
            ('freq_interval', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('begin_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['RecurItem'])

        # Adding model 'CashLevel'
        db.create_table('main_cashlevel', (
            ('cash_level', self.gf('django.db.models.fields.FloatField')()),
            ('date', self.gf('django.db.models.fields.DateField')(unique=True, primary_key=True)),
        ))
        db.send_create_signal('main', ['CashLevel'])

        # Adding model 'Ledger'
        db.create_table('main_ledger', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('exp_inc', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('recur_item', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['main.RecurItem'], null=True)),
        ))
        db.send_create_signal('main', ['Ledger'])

        # Adding unique constraint on 'Ledger', fields ['name', 'date']
        db.create_unique('main_ledger', ['name', 'date'])


    def backwards(self, orm):
        # Removing unique constraint on 'Ledger', fields ['name', 'date']
        db.delete_unique('main_ledger', ['name', 'date'])

        # Deleting model 'RecurItem'
        db.delete_table('main_recuritem')

        # Deleting model 'CashLevel'
        db.delete_table('main_cashlevel')

        # Deleting model 'Ledger'
        db.delete_table('main_ledger')


    models = {
        'main.cashlevel': {
            'Meta': {'object_name': 'CashLevel'},
            'cash_level': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True', 'primary_key': 'True'})
        },
        'main.ledger': {
            'Meta': {'unique_together': "(('name', 'date'),)", 'object_name': 'Ledger', 'ordering': "['date', 'name']"},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'exp_inc': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'recur_item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['main.RecurItem']", 'null': 'True'})
        },
        'main.recuritem': {
            'Meta': {'object_name': 'RecurItem'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'exp_inc': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'freq_interval': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'freq_num': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'primary_key': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['main']