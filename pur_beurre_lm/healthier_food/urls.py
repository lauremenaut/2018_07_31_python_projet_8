#! /usr/bin/env python3
# coding: utf-8

from django.urls import path

from . import views

urlpatterns = [
    path('search', views.search, name='search'),
    path('substitute/<int:unhealthy_product_code>', views.substitute, name='substitute'),
    path('details/<int:product_code>', views.details, name='details'),
    path('new_account', views.new_account, name='new_account'),
    path('account_creation', views.account_creation, name='account_creation'),
    path('login', views.login_user, name='login'),
    path('my_account', views.my_account, name='my_account'),
    path('favorites', views.favorites, name='favorites'),
    path('add_favorite/<int:favorite_code>', views.add_favorite, name='add_favorite'),
    path('logout', views.logout_user, name='logout'),
]
