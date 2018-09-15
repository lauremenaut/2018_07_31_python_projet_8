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

from django.forms import ModelForm, TextInput, PasswordInput
from django.contrib.auth.models import User


class NewAccountForm(ModelForm):

    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'})
        }
