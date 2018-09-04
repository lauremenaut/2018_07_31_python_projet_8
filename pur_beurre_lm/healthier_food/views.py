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
    # Le système lui propose des produits non sains qui correspondent à la recherche
    # L'utilisateur clique sur un des produits non sains
    # Le système affiche le meilleur substitut

    query = request.GET.get('query')
    unhealthy_products = Product.objects.filter(name__icontains=query).exclude(nutrition_grade="a").exclude(nutrition_grade="b")[:3]

    healthy_products_dict = {}
    unhealthy_healthy_products_dict = {}

    for unhealthy_product in unhealthy_products:
        healthy_products_list = []
        categories = unhealthy_product.categories.all()
        for category in categories:
            healthy_products = Product.objects.filter(categories=category).exclude(nutrition_grade="d").exclude(nutrition_grade="e")
            for healthy_product in healthy_products:
                if healthy_product not in healthy_products_list:
                    healthy_products_list.append(healthy_product)
        for healthy_product in healthy_products_list:
            shared_categories = []
            for category in categories:
                if Category.objects.get(name=category) in healthy_products_list:
                    shared_categories.append(category)
            healthy_products_dict[healthy_product] = len(shared_categories)

        maximum = max(healthy_products_dict.values())

        best_matches = []

        for name, number_of_shared_categories in healthy_products_dict.items():
            if number_of_shared_categories == maximum:
                best_matches.append(name)

        for match in best_matches:
            healthiest_matches = Product.objects.filter(name=match).filter(nutrition_grade="a")

        try:
            if not healthiest_matches:
                raise IndexError
            else:
                healthiest_match = healthiest_matches[randint(0, (len(healthiest_matches) - 1))]

        except IndexError:
            if not best_matches:
                print("Aucun produit sain associé ... ne pas proposer le produit")

            i = randint(0, (len(best_matches) - 1))
            print("len(best_matches) : ", len(best_matches))
            healthiest_match = best_matches[i]

        unhealthy_healthy_products_dict[unhealthy_product] = healthiest_match.code

    template = loader.get_template('healthier_food/search.html')
    return HttpResponse(template.render({'products_dict': unhealthy_healthy_products_dict}, request=request))


def detail(request, product_code):
    code = int(product_code)
    product = Product.objects.get(code=code)
    template = loader.get_template('healthier_food/detail.html')
    return HttpResponse(template.render({'product': product}, request=request))


