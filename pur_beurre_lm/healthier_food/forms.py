#! /usr/bin/env python3
# coding: utf-8

from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.models import User


class NewAccountForm(ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : Jean'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : Martin'}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : j.martin'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex : jean.martin@email.com'}),
            'password': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ex : 32hg65ez98hj'})
        }
