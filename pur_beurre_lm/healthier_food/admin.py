#! /usr/bin/env python3
# coding: utf-8

from django.contrib import admin

from .models import Product, Category, Favorite  #, PurBeurreUser


class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'brand', 'nutriscore')
    list_filter = ('nutriscore',)
    search_fields = ('name', 'description', 'brand')
    prepopulated_fields = {'slug': ('name', ), }

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Favorite)
# admin.site.register(PurBeurreUser)
