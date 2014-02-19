# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Usuario'
        db.create_table('usuario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='nu_usuario')),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_column='co_usuario', db_index=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(db_column='fl_activo')),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(db_column='fl_administrador')),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=40, db_column='co_clave')),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(null=True, db_column='fe_ultimoacceso', blank=True)),
            ('nombres', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='no_nombres')),
            ('apellidoPaterno', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='no_apellidopaterno')),
            ('apellidoMaterno', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='no_apellidomaterno')),
        ))
        db.send_create_signal(u'auth', ['Usuario'])

    def backwards(self, orm):
        # Deleting model 'Usuario'
        db.delete_table('usuario')

    models = {
        u'auth.usuario': {
            'Meta': {'object_name': 'Usuario', 'db_table': "'usuario'"},
            'apellidoMaterno': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'no_apellidomaterno'"}),
            'apellidoPaterno': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'no_apellidopaterno'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'nu_usuario'"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'db_column': "'fl_activo'"}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'db_column': "'fl_administrador'"}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'fe_ultimoacceso'", 'blank': 'True'}),
            'nombres': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'no_nombres'"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_column': "'co_clave'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_column': "'co_usuario'", 'db_index': 'True'})
        },
    }

    complete_apps = ['auth']