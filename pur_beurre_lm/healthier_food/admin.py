#! /usr/bin/env python3
# coding: utf-8

from django.contrib import admin

from .models import Product, Category, Favorite

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Favorite)
