# -*- coding: utf-8 -*-
__author__ = 'holivares'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=8, widget=forms.TextInput(attrs={
        'data-original-title': 'Escriba su DNI',
        'data-placement': 'top',
        'placeholder': 'Escriba su DNI'
    }))
    password = forms.CharField(max_length=10,widget=forms.PasswordInput(attrs={
        'data-original-title': u'Escriba su fecha de nacmiento. El formato será dd-mm-yyyy',
        'data-placement': 'top',
        'placeholder': 'Escriba su Fecha de Nacimiento'
    }))