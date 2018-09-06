from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from random import randint

from .models import Product, Category

def home(request):
    template = loader.get_template('healthier_food/home.html')
    return HttpResponse(template.render(request=request))


def search(request):
    # L'utilisateur saisit un mot
    # Le système lui propose des produits non sains qui correspondent à la recherche (6 max)

    unhealthy_products_list = []

    query = request.GET.get('query')
    unhealthy_products = Product.objects.filter(name__icontains=query).exclude(nutrition_grade="a").exclude(nutrition_grade="b")[:6]

    for unhealthy_product in unhealthy_products:
        unhealthy_products_list.append(unhealthy_product)

    if len(unhealthy_products_list) < 6:
        more_unhealthy_products = Product.objects.filter(description__icontains=query).exclude(nutrition_grade="a").exclude(nutrition_grade="b")[:6]

        try:
            i = 0
            while len(unhealthy_products_list) < 6:
                if more_unhealthy_products[i] not in unhealthy_products_list:
                    unhealthy_products_list.append(more_unhealthy_products[i])
                i += 1
        except IndexError:
            pass

    if len(unhealthy_products_list) < 6:
        more_unhealthy_products = Product.objects.filter(brand__icontains=query).exclude(nutrition_grade="a").exclude(nutrition_grade="b")[:6]

        try:
            i = 0
            while len(unhealthy_products_list) < 6:
                if more_unhealthy_products[i] not in unhealthy_products_list:
                    unhealthy_products_list.append(more_unhealthy_products[i])
                i += 1
        except IndexError:
            pass

    template = loader.get_template('healthier_food/search.html')
    return HttpResponse(template.render({'unhealthy_products': unhealthy_products_list}, request=request))

def substitute(request, unhealthy_product_code):
    # L'utilisateur a cliqué sur un des produits non sains
    # Le système affiche les meilleurs substituts (6 max)

    unhealthy_product = Product.objects.get(code=unhealthy_product_code)

    # Get healthy products sharing at least one category with unhealthy_product
    healthy_products_list = []
    categories = unhealthy_product.categories.all()
    for category in categories:
        healthy_products = Product.objects.filter(categories=category).exclude(nutrition_grade="d").exclude(nutrition_grade="e")
        for healthy_product in healthy_products:
            if healthy_product not in healthy_products_list:
                healthy_products_list.append(healthy_product)

    # Count shared categories between healthy and unhealthy products
    shared_categories_counter = {}
    for healthy_product in healthy_products_list:
        shared_categories = []
        for category in categories:
            if Category.objects.get(name=category) in healthy_products:
                shared_categories.append(category)
        shared_categories_counter[healthy_product] = len(shared_categories)

    maximum = max(shared_categories_counter.values())

    best_matches = []

    for healthy_product, number_of_shared_categories in shared_categories_counter.items():
        if number_of_shared_categories == maximum and len(best_matches) < 6:
            best_matches.append(healthy_product)

    healthiest_matches_list = []

    for match in best_matches:
            healthiest_matches = Product.objects.filter(name=match).filter(nutrition_grade="a")[:6]
            for healthiest_match in healthiest_matches:
                healthiest_matches_list.append(healthiest_match)

    i = 0
    while len(healthiest_matches_list) < 6:
        if best_matches[i] not in healthiest_matches_list:
            healthiest_matches_list.append(best_matches[i])
        i += 1

    template = loader.get_template('healthier_food/substitute.html')
    return HttpResponse(template.render({'unhealthy_product': unhealthy_product, 'healthy_products': healthiest_matches_list}, request=request))


def detail(request, product_code):
    code = int(product_code)
    product = Product.objects.get(code=code)
    template = loader.get_template('healthier_food/detail.html')
    return HttpResponse(template.render({'product': product}, request=request))


