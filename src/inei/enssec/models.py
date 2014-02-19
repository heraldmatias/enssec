# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError

__author__ = 'holivares'

from django.db import models
from inei.auth.models import Usuario


OPTIONS1 = (
    (1, u'Información/asesoría'),
    (2, u'DNI, registro de nacimiento o similar'),
    (3, u'Pasaporte/salvoconducto'),
    (4, u'Escritura pública, legizlaciones o similar'),
    (5, u'Asistencia y apoyo humanitario'),
    (6, u'Otro'),
)

OPTIONS2 = (
    (1, u'Muy Bueno'),
    (2, u'Bueno'),
    (3, u'Regular'),
    (4, u'Malo'),
    (5, u'Muy Malo'),
)

OPTIONS3 = (
    (1, u'Muy rápido'),
    (2, u'Rápido'),
    (3, u'Moderado'),
    (4, u'Demora un poco'),
    (5, u'Demora en exceso'),
)

OPTIONS5 = (
    (1, u'Muy satisfecho'),
    (2, u'Satisfecho'),
    (3, u'Ni satisfecho ni insatisfecho'),
    (4, u'Insatisfecho'),
    (5, u'Muy insatisfecho'),
)

OPTIONS6 = (
    (1, u'Contratando más personal'),
    (2, u'Mejorando la comunicación (teléfono/internet)'),
    (3, u'Mejorando la infraestructura y mobiliario'),
    (4, u'Capacitando al personal'),
    (5, u'Mayores horarios de atención'),
    (6, 'Otro')
)

SEXO = (
    (1, 'Hombre'),
    (2, 'Mujer')
)


def validate_edad(value):
    if value < 18:
        raise ValidationError('Su edad debe ser mayor a 18')


def validate_dni(value):
    if len(value) <> 8:
        raise ValidationError(u'El número de DNI debe ser de 8 caracteres')


class Continente(models.Model):
    id = models.CharField(primary_key=True, max_length=4, db_column='co_continente')
    nombre = models.CharField(unique=True, max_length=10, db_column='no_continente')

    class Meta:
        ordering = ('nombre', )
        db_table = 'continente'

    def __unicode__(self):
        return u'%s' % self.nombre


class Consulado(models.Model):
    id = models.CharField(primary_key=True, max_length=2, db_column='co_consulado')
    continente = models.ForeignKey(Continente, db_column='co_continente')
    nombre = models.CharField(max_length=150, db_column='no_consulado')

    class Meta:
        db_table = 'consulado'
        ordering = ('nombre', )

    def __unicode__(self):
        return u'%s' % self.nombre


class Pais(models.Model):
    id = models.CharField(primary_key=True, max_length=4, db_column='co_pais')
    continente = models.ForeignKey(Continente, db_column='co_continente')
    nombre = models.CharField(unique=True, max_length=20, db_column='no_pais')
    nombreOficial = models.CharField(max_length=70, db_column='no_oficial')
    capital = models.CharField(max_length=20, db_column='no_capital')

    class Meta:
        db_table = 'pais'
        ordering = ('nombre', )

    def __unicode__(self):
        return u'%s' % self.nombre


class Cuestionario(models.Model):
    id = models.CharField(primary_key=True, max_length=4, db_column='co_ficha')
    fecha = models.DateField(db_column='fe_encuesta', verbose_name='Fecha de la encuesta')
    edad = models.IntegerField(blank=True, null=True, db_column='nu_edad', validators=[validate_edad])
    ciudadResidencia = models.CharField(max_length=70, db_column='no_ciudadresidencia')
    sexo = models.SmallIntegerField(db_column='fl_sexo', choices=SEXO)
    nu_respuesta1 = models.CommaSeparatedIntegerField(max_length=20, db_column='nu_respuesta1')
    no_respuesta1_6 = models.CharField(max_length=70, blank=True, db_column='no_respuesta1_6')
    nu_respuesta2 = models.SmallIntegerField(db_column='nu_respuesta2', choices=OPTIONS2)
    nu_respuesta3 = models.SmallIntegerField(db_column='nu_respuesta3', choices=OPTIONS3)
    nu_respuesta4 = models.SmallIntegerField(db_column='nu_respuesta4', choices=OPTIONS2)
    nu_respuesta5 = models.SmallIntegerField(db_column='nu_respuesta5', choices=OPTIONS5)
    nu_respuesta6 = models.SmallIntegerField(db_column='nu_respuesta6', choices=OPTIONS6)
    no_respuesta6 = models.CharField(max_length=70, blank=True, db_column='no_respuesta6')
    encuestado = models.CharField(max_length=100, db_column='no_nombreencuestado')
    dni = models.CharField(max_length=8, db_column='co_dni', validators=[validate_dni])
    observacion = models.TextField(blank=True, db_column='tx_observacion')
    pais = models.ForeignKey('Pais', db_column='co_pais', verbose_name=u'País de Residencia')
    consulado = models.ForeignKey(Consulado, db_column='co_consulado', verbose_name='Nombre del consulado')
    continente = models.ForeignKey(Continente, db_column='co_continente')
    usuario = models.ForeignKey(Usuario, db_column='nu_usuario')

    class Meta:
        db_table = 'cuestionario'