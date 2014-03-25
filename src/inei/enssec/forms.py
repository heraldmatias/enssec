# -*- coding: utf-8 -*-
from django.forms.extras.widgets import SelectDateWidget
from django.forms.fields import MultipleChoiceField

__author__ = 'holivares'
import datetime
import re

from django.forms.widgets import RadioFieldRenderer, CheckboxSelectMultiple, CheckboxFieldRenderer
from django import forms
from inei.enssec.models import Cuestionario, Consulado, Pais
from django.core.cache import cache
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.formats import get_format
from django.utils import six
from django.conf import settings
from django.utils import datetime_safe


RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')
MONTHS = {
    1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06',
    7: '07', 8: '08', 9: '09', 10: '10', 11: '11',
    12: '12'
}

class RadioFieldRenderer2(RadioFieldRenderer):

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            if not choice[0] == '' or choice[0] is None:
                yield self.choice_input_class(self.name, self.value, self.attrs.copy(), choice, i)


class CheckboxFieldRenderer2(CheckboxFieldRenderer):

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            if not choice[0] == '' or choice[0] is None:
                yield self.choice_input_class(self.name, self.value, self.attrs.copy(), choice, i)


def getConsuladoChoices():
    if cache.get('consulados'):
        choices = cache.get('consulados')
    else:
        choices = [('%s-%s-%s' % (c[0], c[1], c[2]), c[3]) for c in Consulado.objects.all().values_list('id', 'continente', 'continente__nombre', 'nombre')]
        choices.insert(0, ('', '-----------------------------'))
        cache.set('consulados', choices, 60)
    return choices


def getPaisChoices():
    if cache.get('pais'):
        choices = cache.get('pais')
    else:
        choices = [('%s-%s-%s' % (c[0], c[1], c[2]), c[3]) for c in Pais.objects.all().values_list('id', 'continente', 'continente__nombre', 'nombre')]
        choices.insert(0, ('', '-----------------------------'))
        cache.set('pais', choices, 60)
    return choices


class CSICheckboxSelectMultiple(CheckboxSelectMultiple):
    def value_from_datadict(self, data, files, name):
        # Return a string of comma separated integers since the database, and
        # field expect a string (not a list).
        return ','.join(data.getlist(name))

    def render(self, name, value, attrs=None, choices=()):
        # Convert comma separated integer string to a list, since the checkbox
        # rendering code expects a list (not a string)
        if value:
            value = value.split(',')
        return super(CSICheckboxSelectMultiple, self).render(
            name, value, attrs=attrs, choices=choices
        )


# Form field
class CSIMultipleChoiceField(MultipleChoiceField):
    widget = CSICheckboxSelectMultiple

    # Value is stored and retrieved as a string of comma separated
    # integers. We don't want to do processing to convert the value to
    # a list like the normal MultipleChoiceField does.
    def to_python(self, value):
        return value

    def validate(self, value):
        # If we have a value, then we know it is a string of comma separated
        # integers. To use the MultipleChoiceField validator, we first have
        # to convert the value to a list.
        if value:
            value = value.split(',')
        super(CSIMultipleChoiceField, self).validate(value)


class CustomSelectDateWidget(SelectDateWidget):
    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, six.string_types):
                if settings.USE_L10N:
                    try:
                        input_format = get_format('DATE_INPUT_FORMATS')[0]
                        v = datetime.datetime.strptime(force_str(value), input_format)
                        year_val, month_val, day_val = v.year, v.month, v.day
                    except ValueError:
                        pass
                else:
                    match = RE_DATE.match(value)
                    if match:
                        year_val, month_val, day_val = [int(v) for v in match.groups()]
        choices = [(i, i) for i in self.years]
        year_html = self.create_select(name, self.year_field, value, year_val, choices)
        choices = list(six.iteritems(MONTHS))
        month_html = self.create_select(name, self.month_field, value, month_val, choices)
        choices = [(i, i) for i in range(1, 32)]
        day_html = self.create_select(name, self.day_field, value, day_val,  choices)

        output = []
        for field in forms.extras.widgets._parse_date_fmt():
            if field == 'year':
                output.append(year_html)
            elif field == 'month':
                output.append(month_html)
            elif field == 'day':
                output.append(day_html)
        return mark_safe('\n'.join(output))

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if y == m == d == "0":
            return None
        if y and m and d:
            if settings.USE_L10N:
                input_format = get_format('DATE_INPUT_FORMATS')[0]
                try:
                    date_value = datetime.date(2000+int(y), int(m), int(d))
                except ValueError:
                    return '%s-%s-%s' % (y, m, d)
                else:
                    date_value = datetime_safe.new_date(date_value)
                    return date_value.strftime(input_format)
            else:
                return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)


class CuestionarioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CuestionarioForm, self).__init__(*args, **kwargs)
        self.fields['consulado_list'] = forms.ChoiceField(choices=getConsuladoChoices())
        self.fields['pais_list'] = forms.ChoiceField(choices=getPaisChoices())
        if self.data.get('nu_respuesta1_6'):
            if self.data.get('nu_respuesta1_6') == '1':
                self.fields['no_respuesta1_6'].required = True
                self.fields['no_respuesta1_6'].widget.attrs['readonly'] = False
            else:
                self.fields['no_respuesta1_6'].widget.attrs['readonly'] = True
        else:
            self.fields['no_respuesta1_6'].widget.attrs['readonly'] = True
        if self.data.get('nu_respuesta6'):
            if self.data.get('nu_respuesta6') == '6':
                self.fields['no_respuesta6'].required = True
                self.fields['no_respuesta1_6'].widget.attrs['readonly'] = False
            else:
                self.fields['no_respuesta6'].widget.attrs['readonly'] = True
        else:
            self.fields['no_respuesta6'].widget.attrs['readonly'] = True

    class Meta:
        model = Cuestionario
        widgets = {
            'nu_respuesta1_1': forms.TextInput(attrs={'class': 'span1 numero bit'}),
            'nu_respuesta1_2': forms.TextInput(attrs={'class': 'span1 numero bit'}),
            'nu_respuesta1_3': forms.TextInput(attrs={'class': 'span1 numero bit'}),
            'nu_respuesta1_4': forms.TextInput(attrs={'class': 'span1 numero bit'}),
            'nu_respuesta1_5': forms.TextInput(attrs={'class': 'span1 numero bit'}),
            'nu_respuesta1_6': forms.TextInput(attrs={'class': 'span1 numero bit'}),
            'no_respuesta1_6': forms.TextInput(attrs={'class': 'span12 texto'}),
            'nu_respuesta2': forms.TextInput(attrs={'class': 'span1 numero'}),
            'nu_respuesta3': forms.TextInput(attrs={'class': 'span1 numero'}),
            'nu_respuesta4': forms.TextInput(attrs={'class': 'span1 numero'}),
            'nu_respuesta5': forms.TextInput(attrs={'class': 'span1 numero'}),
            'nu_respuesta6': forms.TextInput(attrs={'class': 'span1 numero'}),
            'no_respuesta6': forms.TextInput(attrs={'class': 'span12 texto'}),
            'tomo': forms.TextInput(attrs={'class': 'span3   numero'}),
            'fecha': CustomSelectDateWidget(years=(13, 14)),
            'edad': forms.TextInput(attrs={'class': 'span12 numero', 'maxlength': 2}),
            'dni': forms.TextInput(attrs={'class': 'span12 numero'}),
            'sexo': forms.Select(attrs={'class': 'span12'}),
            'encuestado': forms.TextInput(attrs={'class': 'span12 texto'}),
            'observacion': forms.Textarea(attrs={'class': 'span12 texto', 'rows': 2}),
            'ciudadResidencia': forms.TextInput(attrs={'class': 'span12 texto'}),
            'ficha': forms.TextInput(attrs={'class': 'span6 numero'})
        }
        exclude = ('usuario', 'continentePais', 'continenteConsulado', 'consulado', 'pais', )