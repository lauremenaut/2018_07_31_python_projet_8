#! /usr/bin/env python3
# coding: utf-8

""" Set DbFiller class.

DbFiller class fills local PostgreSQL database retrieving data from
Open Food Facts API.

"""
from django.db.utils import DataError, IntegrityError

from requests import get

from .params import nutrition_grades, tag_categories
from .models import Category, Store, Product


class DbFiller:

    """ Set DbFiller class. """

    def __init__(self):
        """ DbFiller constructor.

        For each category and for each nutrition grade, retrieve
        corresponding products from Open Food Facts API and add them to
        local database.

        """
        for nutrition_grade in nutrition_grades:
            for category in tag_categories:
                products = self._get_products(category, nutrition_grade)
                self._fill_db(products)

    def _get_products(self, category, nutrition_grade):
        """ Return a list of dictionnaries of products information.

        Connect to Open Food Facts API via get() method from requests
        library and send requests using given criteria for categories
        and nutrition grades.
        json content from response object contains products information.

        """
        criteria = {
            'action': 'process',
            'json': 1,
            'countries': 'France',
            'page_size': 100,
            'page': 1,
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category,
            'tagtype_1': 'nutrition_grades',
            'tag_contains_1': 'contains',
            'tag_1': nutrition_grade
            }

        response = get('https://fr.openfoodfacts.org/cgi/search.pl',
                       params=criteria)
        data = response.json()

        # 'products' is a list of dictionnaries
        products = data['products']
        return products

    def _fill_db(self, products):
        """ Manage database filling.

        Check for each product whether required data is available or
        not.
        If so, product is added to local database.

        """
        for product in products:
            try:
                self.code = product['code']
                self.name = product['product_name'].strip().capitalize()
                self.description = product['generic_name'].capitalize()
                brands = (product['brands']).split(',')
                self.brand = brands[0].capitalize()
                self.url = product['url']
                self.nutrition_grade = product['nutrition_grades'].lower()
                self.image = product['image_url']
                # self.image = product['image_small_url']
                self.energy = product['energy_100g']
                categories_to_strip = (product['categories']).split(',')
                self.categories = []
                for category in categories_to_strip:
                    self.categories.append(category.strip().capitalize())
                stores_to_strip = (product['stores']).split(',')
                self.stores = []
                for store in stores_to_strip:
                    self.stores.append(store.strip().capitalize())

            except KeyError:
                print('Missing data', file=open('print_log.txt', 'a'))

# Remplacer 'print' par 'logging'

            if all([self.code, self.name, self.description, self.brand,
                    self.url, self.nutrition_grade,self.image, self.energy, self.categories[0],
                    self.stores[0]]):

                try:
                    new_product = Product(code=self.code, name=self.name,
                                          description=self.description,
                                          brand=self.brand, url=self.url,
                                          nutrition_grade=self.nutrition_grade)
                    new_product.save()

                    for category in self.categories:
                        Category.objects.create(name=category)
                        new_category = Category.objects.get(name=category)
                        new_product.categories.add(new_category.id)

                    for store in self.stores:
                        Store.objects.create(name=store)
                        new_store = Store.objects.get(name=store)
                        new_product.stores.add(new_store.id)

                except IntegrityError as e:
                    print("IntegrityError : ", e, file=open('print_log.txt', 'a'))

                except DataError as e:
                    print("DataError : ", e, file=open('print_log.txt', 'a'))
