#! /usr/bin/env python3
# coding: utf-8

""" Set DbFiller class.

DbFiller class fills local PostgreSQL database retrieving data from
Open Food Facts API.

"""
from django.db.utils import DataError, IntegrityError

from requests import get

from .params import nutriscores, tag_categories
from .models import Category, Product


class DbFiller:

    """ Set DbFiller class. """

    def __init__(self):
        """ DbFiller constructor.

        For each category and for each nutrition grade, retrieve
        corresponding products from Open Food Facts API and add them to
        local database.

        """
        for nutriscore in nutriscores:
            for category in tag_categories:
                products = self._get_products(category, nutriscore)
                self._fill_db(products)

    def _get_products(self, category, nutriscore):
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
            'tag_1': nutriscore
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
        try:
            for product in products:
                self.code = product['code']
                self.name = product['product_name'].strip().capitalize()
                self.description = product['generic_name'].capitalize()
                brands = (product['brands']).split(',')
                self.brand = brands[0].capitalize()
                self.url = product['url']
                self.nutriscore = product['nutrition_grades'].upper()
                self.image = product['image_url']
                # self.image_small = product['image_small_url']

                categories_to_strip = (product['categories']).split(',')
                self.categories = []
                for category in categories_to_strip:
                    self.categories.append(category.strip().capitalize())

                if all([self.code, self.name, self.description, self.brand,
                        self.url, self.nutriscore, self.image, self.image_small, self.categories[0]]):

                    new_product = Product(code=self.code, name=self.name,
                                          description=self.description,
                                          brand=self.brand, url=self.url,
                                          nutriscore=self.nutriscore,
                                          image=self.image)
                    new_product.save()

                    for category in self.categories:
                        existing_category = Category.objects.filter(name=category)
                        if existing_category:
                            new_product.categories.add(existing_category[0].id)
                        else:
                            Category.objects.create(name=category)
                            new_category = Category.objects.get(name=category)
                            new_product.categories.add(new_category.id)

        except KeyError as e:
            print('KeyError : ', e)
            # print('Missing data', file=open('print_log.txt', 'a'))

        except AttributeError as e:
            print("AttributeError : ", e)
            # print("IntegrityError : ", e, file=open('print_log.txt', 'a'))

        except IntegrityError as e:
            print("IntegrityError : ", e)
            # print("IntegrityError : ", e, file=open('print_log.txt', 'a'))

        except DataError as e:
            print("DataError : ", e)
            # print("DataError : ", e, file=open('print_log.txt', 'a'))
