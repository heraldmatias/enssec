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
    if value not in ('1', '2', '3', '4', '5', '9'):
        raise ValidationError(u'Debe ingresar solo 1 a 5')


def validate_16(value):
    if value not in ('1', '2', '3', '4', '5', '6', '9'):
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
    tomo = models.CharField(max_length=2, db_column='nu_tomo')
    fecha = models.CharField(max_length=10, db_column='fe_encuesta', verbose_name='Fecha de la encuesta')
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
    dni = models.CharField(max_length=8, db_column='co_dni', validators=[validate_dni], unique=True, null=True, blank=True)
    observacion = models.TextField(blank=True, db_column='tx_observacion')
    pais = models.CharField(max_length=4, db_column='co_pais', verbose_name=u'País de Residencia')
    consulado = models.CharField(max_length=2, db_column='co_consulado', verbose_name='Nombre del consulado')
    continentePais = models.CharField(max_length=4, db_column='co_continentepais')
    continenteConsulado = models.CharField(max_length=4, db_column='co_continenteconsulado')
    usuario = models.ForeignKey(User, db_column='nu_usuario')
    fecha_registro = models.DateField(db_column='fe_registro', verbose_name='Fecha de registro', auto_now_add=True)

    def validate_unique(self, exclude=None):
        """
        Checks unique constraints on the model and raises ``ValidationError``
        if any failed.
        """
        unique_checks, date_checks = self._get_unique_checks(exclude=exclude)
        errors = self._perform_unique_checks(unique_checks)
        date_errors = self._perform_date_checks(date_checks)

        for k, v in date_errors.items():
            errors.setdefault(k, []).extend(v)

        if errors:
            if 'dni' in errors:
                if self.dni == '' or self.dni is None:
                    del errors['dni']
                else:
                    cuestionario = Cuestionario.objects.filter(dni=self.dni)
                    cuestionario = cuestionario.values('tomo', 'ficha')[0]
                    msg = u'Ya existe el DNI en el siguiente tomo %s y ficha %s' % (cuestionario['tomo'], cuestionario['ficha'])
                    errors['dni'][0] = msg
            raise ValidationError(errors)

    def _get_unique_checks(self, exclude=None):
        """
        Gather a list of checks to perform. Since validate_unique could be
        called from a ModelForm, some fields may have been excluded; we can't
        perform a unique check on a model that is missing fields involved
        in that check.
        Fields that did not validate should also be excluded, but they need
        to be passed in via the exclude argument.
        """
        if exclude is None:
            exclude = []
        unique_checks = []

        unique_togethers = [(self.__class__, self._meta.unique_together)]
        for parent_class in self._meta.parents.keys():
            if parent_class._meta.unique_together:
                unique_togethers.append((parent_class, parent_class._meta.unique_together))

        for model_class, unique_together in unique_togethers:
            for check in unique_together:
                unique_checks.append((model_class, tuple(check)))
        # These are checks for the unique_for_<date/year/month>.
        date_checks = []

        # Gather a list of checks for fields declared as unique and add them to
        # the list of checks.

        fields_with_class = [(self.__class__, self._meta.local_fields)]
        for parent_class in self._meta.parents.keys():
            fields_with_class.append((parent_class, parent_class._meta.local_fields))

        for model_class, fields in fields_with_class:
            for f in fields:
                name = f.name
                if name in exclude:
                    continue
                if f.unique:
                    unique_checks.append((model_class, (name,)))
                if f.unique_for_date and f.unique_for_date not in exclude:
                    date_checks.append((model_class, 'date', name, f.unique_for_date))
                if f.unique_for_year and f.unique_for_year not in exclude:
                    date_checks.append((model_class, 'year', name, f.unique_for_year))
                if f.unique_for_month and f.unique_for_month not in exclude:
                    date_checks.append((model_class, 'month', name, f.unique_for_month))
        return unique_checks, date_checks

    class Meta:
        db_table = 'cuestionario'
        unique_together = ('ficha', 'tomo', 'consulado', 'continenteConsulado',)


class UsuarioConsulado(models.Model):
    id = models.AutoField(primary_key=True, db_column='nu_usuarioconsulado')
    usuario = models.ForeignKey(User, db_column='nu_usuario')
    consulado = models.CharField(max_length=2, db_column='co_consulado')
    continente = models.ForeignKey(Continente, db_column='co_continente')
    tomo = models.IntegerField(db_column='nu_tomo')

    class Meta:
        db_table = 'usuarioconsulado'


class TotalDigitacion(models.Model):
    fecha = models.DateField(db_column='fecha', verbose_name='Fecha de la encuesta')
    digitador = models.CharField(max_length=60, db_column='digitador_nombre')
    usuario = models.CharField(max_length=30, db_column='digitador_usuario')
    consulado = models.CharField(max_length=70, db_column='consulado')
    fichas = models.IntegerField(db_column='fichas')

    class Meta:
        managed = False
        db_table = 'lv_total_digitacion'


class ResumenDigitacion(models.Model):
    fecha = models.DateField(db_column='fecha', verbose_name='Fecha de la encuesta')
    digitador = models.CharField(max_length=60, db_column='digitador_nombre')
    codigo_digitador = models.IntegerField(db_column='codigo_digitador')
    usuario = models.CharField(max_length=30, db_column='digitador_usuario')
    ficha = models.CharField(max_length=4, db_column='ficha')
    consulado = models.CharField(max_length=70, db_column='no_consulado')
    tomo = models.CharField(max_length=2, db_column='tomo')

    class Meta:
        managed = False
        db_table = 'lv_resumen_digitacion'


class TotalDigitacionConsulado(models.Model):
    consulado = models.CharField(max_length=30, db_column='no_consulado')
    tomo = models.IntegerField(db_column='nu_tomo')
    meta = models.IntegerField(db_column='nu_meta')
    encuestas = models.IntegerField(db_column='nu_encuestas')
    recepcionado = models.IntegerField(db_column='nu_recepcionado')
    repetidos = models.IntegerField(db_column='nu_fichasrepetidas')
    fichas = models.IntegerField(db_column='fichas')

    class Meta:
        managed = False
        db_table = 'lv_total_digitacion_consulado'