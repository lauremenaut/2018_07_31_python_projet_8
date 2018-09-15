#! /usr/bin/env python3
# coding: utf-8

from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^search/$', views.search, name='search'),
    re_path(r'^substitute/(?P<unhealthy_product_code>[0-9]+)/$', views.substitute, name='substitute'),
    re_path(r'^details/(?P<product_code>[0-9]+)/$', views.details, name='details'),
    re_path(r'^new_account/$', views.new_account, name='new_account'),
    re_path(r'^account_creation/$', views.account_creation, name='account_creation'),
    re_path(r'^login/$', views.login_user, name='login'),
    re_path(r'^my_account/$', views.my_account, name='my_account'),
    re_path(r'^favorites/$', views.favorites, name='favorites'),
    re_path(r'^add_favorite/(?P<favorite_code>[0-9]*)/$', views.add_favorite, name='add_favorite'),
    re_path(r'^logout/$', views.logout_user, name='logout'),
]
