# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Continente'
        db.create_table('continente', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True, db_column='co_continente')),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10, db_column='no_continente')),
        ))
        db.send_create_signal(u'enssec', ['Continente'])

        # Adding model 'Consulado'
        db.create_table('consulado', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True, db_column='co_consulado')),
            ('continente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enssec.Continente'], db_column='co_continente')),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=150, db_column='no_consulado')),
        ))
        db.send_create_signal(u'enssec', ['Consulado'])

        # Adding model 'Pais'
        db.create_table('pais', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True, db_column='co_pais')),
            ('continente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enssec.Continente'], db_column='co_continente')),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, db_column='no_pais')),
            ('nombreOficial', self.gf('django.db.models.fields.CharField')(max_length=70, db_column='no_oficial')),
            ('capital', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='no_capital')),
        ))
        db.send_create_signal(u'enssec', ['Pais'])

        # Adding model 'Cuestionario'
        db.create_table('cuestionario', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(db_column='fe_encuesta')),
            ('edad', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='nu_edad', blank=True)),
            ('ciudadResidencia', self.gf('django.db.models.fields.CharField')(max_length=70, db_column='no_ciudadresidencia', blank=True)),
            ('sexo', self.gf('django.db.models.fields.SmallIntegerField')(null=True, db_column='fl_sexo', blank=True)),
            ('nu_respuesta1_1', self.gf('django.db.models.fields.SmallIntegerField')(null=True, db_column='nu_respuesta1_1', blank=True)),
            ('nu_respuesta1_2', self.gf('django.db.models.fields.SmallIntegerField')(null=True, db_column='nu_respuesta1_2', blank=True)),
            ('nu_respuesta1_3', self.gf('django.db.models.fields.SmallIntegerField')(null=True, db_column='nu_respuesta1_3', blank=True)),
            ('nu_respuesta1_4', self.gf('django.db.models.fields.SmallIntegerField')(null=True, db_column='nu_respuesta1_4', blank=True)),
            ('nu_respuesta1_5', self.gf('django.db.models.fields.SmallIntegerField')(null=True, db_column='nu_respuesta1_5', blank=True)),
            ('nu_respuesta1_6', self.gf('django.db.models.fields.SmallIntegerField')(null=True, db_column='nu_respuesta1_6', blank=True)),
            ('no_respuesta1_6', self.gf('django.db.models.fields.CharField')(max_length=70, db_column='no_respuesta1_6', blank=True)),
            ('nu_respuesta2', self.gf('django.db.models.fields.SmallIntegerField')(db_column='nu_respuesta2')),
            ('nu_respuesta3', self.gf('django.db.models.fields.SmallIntegerField')(db_column='nu_respuesta3')),
            ('nu_respuesta4', self.gf('django.db.models.fields.SmallIntegerField')(db_column='nu_respuesta4')),
            ('nu_respuesta5', self.gf('django.db.models.fields.SmallIntegerField')(db_column='nu_respuesta5')),
            ('nu_respuesta6', self.gf('django.db.models.fields.SmallIntegerField')(null=True, db_column='nu_respuesta6', blank=True)),
            ('no_respuesta6', self.gf('django.db.models.fields.CharField')(max_length=70, db_column='no_respuesta6', blank=True)),
            ('encuestado', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='no_nombreencuestado')),
            ('dni', self.gf('django.db.models.fields.CharField')(max_length=8, db_column='co_dni')),
            ('observacion', self.gf('django.db.models.fields.TextField')(db_column='tx_observacion', blank=True)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enssec.Pais'], db_column='co_pais')),
            ('co_consulado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enssec.Consulado'], db_column='co_consulado')),
            ('co_continente', self.gf('django.db.models.fields.CharField')(max_length=4, db_column='co_continente')),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Usuario'], db_column='nu_usuario')),
        ))
        db.send_create_signal(u'enssec', ['Cuestionario'])


    def backwards(self, orm):
        # Deleting model 'Continente'
        db.delete_table('continente')

        # Deleting model 'Consulado'
        db.delete_table('consulado')

        # Deleting model 'Pais'
        db.delete_table('pais')

        # Deleting model 'Cuestionario'
        db.delete_table('cuestionario')


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
        u'enssec.consulado': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Consulado', 'db_table': "'consulado'"},
            'continente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['enssec.Continente']", 'db_column': "'co_continente'"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True', 'db_column': "'co_consulado'"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'no_consulado'"})
        },
        u'enssec.continente': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Continente', 'db_table': "'continente'"},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True', 'db_column': "'co_continente'"}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'db_column': "'no_continente'"})
        },
        u'enssec.cuestionario': {
            'Meta': {'object_name': 'Cuestionario', 'db_table': "'cuestionario'"},
            'ciudadResidencia': ('django.db.models.fields.CharField', [], {'max_length': '70', 'db_column': "'no_ciudadresidencia'", 'blank': 'True'}),
            'co_consulado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['enssec.Consulado']", 'db_column': "'co_consulado'"}),
            'co_continente': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_column': "'co_continente'"}),
            'dni': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_column': "'co_dni'"}),
            'edad': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'nu_edad'", 'blank': 'True'}),
            'encuestado': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'no_nombreencuestado'"}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'db_column': "'fe_encuesta'"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'no_respuesta1_6': ('django.db.models.fields.CharField', [], {'max_length': '70', 'db_column': "'no_respuesta1_6'", 'blank': 'True'}),
            'no_respuesta6': ('django.db.models.fields.CharField', [], {'max_length': '70', 'db_column': "'no_respuesta6'", 'blank': 'True'}),
            'nu_respuesta1_1': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'db_column': "'nu_respuesta1_1'", 'blank': 'True'}),
            'nu_respuesta1_2': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'db_column': "'nu_respuesta1_2'", 'blank': 'True'}),
            'nu_respuesta1_3': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'db_column': "'nu_respuesta1_3'", 'blank': 'True'}),
            'nu_respuesta1_4': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'db_column': "'nu_respuesta1_4'", 'blank': 'True'}),
            'nu_respuesta1_5': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'db_column': "'nu_respuesta1_5'", 'blank': 'True'}),
            'nu_respuesta1_6': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'db_column': "'nu_respuesta1_6'", 'blank': 'True'}),
            'nu_respuesta2': ('django.db.models.fields.SmallIntegerField', [], {'db_column': "'nu_respuesta2'"}),
            'nu_respuesta3': ('django.db.models.fields.SmallIntegerField', [], {'db_column': "'nu_respuesta3'"}),
            'nu_respuesta4': ('django.db.models.fields.SmallIntegerField', [], {'db_column': "'nu_respuesta4'"}),
            'nu_respuesta5': ('django.db.models.fields.SmallIntegerField', [], {'db_column': "'nu_respuesta5'"}),
            'nu_respuesta6': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'db_column': "'nu_respuesta6'", 'blank': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'db_column': "'tx_observacion'", 'blank': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['enssec.Pais']", 'db_column': "'co_pais'"}),
            'sexo': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'db_column': "'fl_sexo'", 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Usuario']", 'db_column': "'nu_usuario'"})
        },
        u'enssec.pais': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Pais', 'db_table': "'pais'"},
            'capital': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'no_capital'"}),
            'continente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['enssec.Continente']", 'db_column': "'co_continente'"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True', 'db_column': "'co_pais'"}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_column': "'no_pais'"}),
            'nombreOficial': ('django.db.models.fields.CharField', [], {'max_length': '70', 'db_column': "'no_oficial'"})
        }
    }

    complete_apps = ['enssec']