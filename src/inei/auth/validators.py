import re
from django.core.validators import RegexValidator

__author__ = 'holivares'

comma_separated_str_list_re = re.compile('^[\w,]+$')
validate_comma_separated_str_list = RegexValidator(comma_separated_str_list_re, u'Ingrese los proyectos separados por comas.', 'invalid')