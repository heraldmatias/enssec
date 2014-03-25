# -*- coding: utf-8 -*-
from numpy.oldnumeric.ma import _maximum_operation
from django.core.exceptions import ValidationError

__author__ = 'holivares'

from django.db import models
from django.contrib.auth.models import User


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
    ('1', '1 - Hombre'),
    ('2', '2 - Mujer')
)


def validate_edad(value):
    if value < 18:
        raise ValidationError('Su edad debe ser mayor a 18')


def validate_dni(value):
    if len(value) != 8:
        raise ValidationError(u'El número de DNI debe ser de 8 caracteres')


def validate_bit(value):
    if value not in ('0', '1'):
        raise ValidationError(u'Debe ingresar solo 0 y 1')


def validate_15(value):
    if value not in ('1', '2', '3', '4', '5'):
        raise ValidationError(u'Debe ingresar solo 1 a 5')


def validate_16(value):
    if value not in ('1', '2', '3', '4', '5', '6'):
        raise ValidationError(u'Debe ingresar solo 1 a 6')


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
        # unique_together = ('id', 'continente', )

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
    ficha = models.CharField(max_length=4, db_column='co_ficha')
    tomo = models.IntegerField(max_length=4, db_column='nu_tomo')
    fecha = models.DateField(db_column='fe_encuesta', verbose_name='Fecha de la encuesta')
    edad = models.IntegerField(db_column='nu_edad', validators=[validate_edad], max_length=2)
    ciudadResidencia = models.CharField(max_length=70, db_column='no_ciudadresidencia')
    sexo = models.CharField(db_column='fl_sexo', max_length=1, choices=SEXO)
    nu_respuesta1_1 = models.CharField(max_length=1, db_column='nu_respuesta1_1', validators=[validate_bit])
    nu_respuesta1_2 = models.CharField(max_length=1, db_column='nu_respuesta1_2', validators=[validate_bit])
    nu_respuesta1_3 = models.CharField(max_length=1, db_column='nu_respuesta1_3', validators=[validate_bit])
    nu_respuesta1_4 = models.CharField(max_length=1, db_column='nu_respuesta1_4', validators=[validate_bit])
    nu_respuesta1_5 = models.CharField(max_length=1, db_column='nu_respuesta1_5', validators=[validate_bit])
    nu_respuesta1_6 = models.CharField(max_length=1, db_column='nu_respuesta1_6', validators=[validate_bit])
    no_respuesta1_6 = models.CharField(max_length=70, blank=True, db_column='no_respuesta1_6')
    nu_respuesta2 = models.CharField(db_column='nu_respuesta2', max_length=1, validators=[validate_15])
    nu_respuesta3 = models.CharField(db_column='nu_respuesta3', max_length=1, validators=[validate_15])
    nu_respuesta4 = models.CharField(db_column='nu_respuesta4', max_length=1, validators=[validate_15])
    nu_respuesta5 = models.CharField(db_column='nu_respuesta5', max_length=1, validators=[validate_15])
    nu_respuesta6 = models.CharField(db_column='nu_respuesta6', max_length=1, validators=[validate_16])
    no_respuesta6 = models.CharField(max_length=70, blank=True, db_column='no_respuesta6')
    encuestado = models.CharField(max_length=100, db_column='no_nombreencuestado')
    dni = models.CharField(max_length=8, db_column='co_dni', validators=[validate_dni], unique=True)
    observacion = models.TextField(blank=True, db_column='tx_observacion')
    pais = models.ForeignKey('Pais', db_column='co_pais', verbose_name=u'País de Residencia')
    consulado = models.ForeignKey(Consulado, db_column='co_consulado', verbose_name='Nombre del consulado')
    continentePais = models.ForeignKey(Continente, db_column='co_continentepais', related_name='paisContinente')
    continenteConsulado = models.ForeignKey(Continente, db_column='co_continenteconsulado', related_name='consuladoContinente')
    usuario = models.ForeignKey(User, db_column='nu_usuario')

    class Meta:
        db_table = 'cuestionario'
        unique_together = ('ficha', 'tomo')