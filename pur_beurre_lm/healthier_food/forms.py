#! /usr/bin/env python3
# coding: utf-8

# from django import forms

# class NewAccountForm(forms.Form):
#     username = forms.CharField(
#         label="Nom d'utilisateur",
#         max_length=150,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True
#         )

#     password = forms.Field(
#         label="Mot de passe",
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True
#         )

from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.models import User


class NewAccountForm(ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : j.martin'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex : jean.martin@email.com'}),
            'password': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ex : 32hg65ez98hj'})
        }
