from django.db import models


# class TimestampedModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True  # Une classe abstraite ne peut pas être instanciée. Django ne la considère donc pas comme un modèle à part entière, il ne génère donc pas de migrations


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)

    def __str__(self):
        return self.first_name


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, unique=True)
    brand = models.CharField(max_length=30)
    url = models.URLField(max_length=250, unique=True)
    nutriscore = models.CharField(max_length=1)
    image = models.ImageField()
    # energy = models.IntegerField()
    ingredients = models.CharField(max_length=500, null=True)
    calories = models.IntegerField(null=True)
    fat = models.IntegerField(null=True)
    cholesterol = models.IntegerField(null=True)
    carbohydrates = models.IntegerField(null=True)
    sugars = models.IntegerField(null=True)
    fibers = models.IntegerField(null=True)
    proteins = models.IntegerField(null=True)
    sodium = models.IntegerField(null=True)
    categories = models.ManyToManyField(Category, related_name='products')
    stores = models.ManyToManyField(Store, related_name='products')

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    request_date = models.DateTimeField(auto_now_add=True)
    unhealthy_product = models.CharField(max_length=100)
    healthy_product = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    stores = models.CharField(max_length=100)
    url = models.URLField(max_length=250)

    def __str__(self):
        return self.healthy_product
