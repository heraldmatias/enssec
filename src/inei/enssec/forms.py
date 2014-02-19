# -*- coding: utf-8 -*-
from django.forms.extras.widgets import SelectDateWidget
from django.forms.fields import MultipleChoiceField

__author__ = 'holivares'

from django.forms.widgets import RadioSelect, RadioFieldRenderer, CheckboxSelectMultiple, CheckboxFieldRenderer
from django import forms
from inei.enssec.models import Cuestionario, Consulado, Continente, OPTIONS1
from django.core.cache import cache


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


class CuestionarioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CuestionarioForm, self).__init__(*args, **kwargs)
        self.fields['consulado_list'] = forms.ChoiceField(choices=getConsuladoChoices())
        self.fields['nu_respuesta1'] = CSIMultipleChoiceField(choices=OPTIONS1)

    class Meta:
        model = Cuestionario
        widgets = {
            # 'nu_respuesta1': CheckboxSelectMultiple(renderer=CheckboxFieldRenderer2),
            'nu_respuesta2': RadioSelect(renderer=RadioFieldRenderer2),
            'nu_respuesta3': RadioSelect(renderer=RadioFieldRenderer2),
            'nu_respuesta4': RadioSelect(renderer=RadioFieldRenderer2),
            'nu_respuesta5': RadioSelect(renderer=RadioFieldRenderer2),
            'nu_respuesta6': RadioSelect(renderer=RadioFieldRenderer2),
            'no_respuesta6': forms.TextInput(attrs={'class': 'span12'}),
            'no_respuesta1_6': forms.TextInput(attrs={'class': 'span12'}),
            'fecha': SelectDateWidget(),
            'edad': forms.TextInput(attrs={'class': 'span12'}),
            'sexo': forms.Select(attrs={'class': 'span12'}),
            'encuestado': forms.TextInput(attrs={'class': 'span12'}),
            'observacion': forms.Textarea(attrs={'class': 'span12', 'rows': 2})
        }
        exclude = ('usuario', 'continente', 'consulado', )