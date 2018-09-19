#! /usr/bin/env python3
# coding: utf-8

from django.db import models


# class TimestampedModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True  # Une classe abstraite ne peut pas être instanciée. Django ne la considère donc pas comme un modèle à part entière, il ne génère donc pas de migrations


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class Product(models.Model):
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, unique=True)
    brand = models.CharField(max_length=30)
    url = models.URLField(max_length=255, unique=True)
    nutriscore = models.CharField(max_length=1)
    image = models.URLField()
    # image_small = models.URLField()

    categories = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"


class Favorite(models.Model):
    username = models.CharField(max_length=150)
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True)
    url = models.URLField(max_length=255, null=True)
    nutriscore = models.CharField(max_length=1, null=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
