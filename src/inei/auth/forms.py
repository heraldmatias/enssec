# -*- coding: utf-8 -*-
__author__ = 'holivares'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=8, widget=forms.TextInput(attrs={
        'data-original-title': 'Escriba su usuario',
        'data-placement': 'top',
        'placeholder': 'Ingrese su usuario'
    }))
    password = forms.CharField(max_length=10,widget=forms.PasswordInput(attrs={
        'data-original-title': u'Escriba su contraseña',
        'data-placement': 'top',
        'placeholder': 'Ingrese su contraseña'
    }))