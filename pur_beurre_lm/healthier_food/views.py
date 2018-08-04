from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Product

def home(request):
    template = loader.get_template('healthier_food/home.html')
    return HttpResponse(template.render(request=request))


def detail(request, product_code):
    code = int(product_code)
    product = Product.objects.get(code=code)
    template = loader.get_template('healthier_food/detail.html')
    return HttpResponse(template.render({'product': product}, request=request))


def search(request):
    # L'utilisateur saisit un mot
    # Le système lui propose des produits non sains qui correspondent à la recherche

    query = request.GET.get('query')
    unhealthy_products = Product.objects.filter(name__icontains=query).exclude(nutrition_grade="a").exclude(nutrition_grade="b")
    template = loader.get_template('healthier_food/search.html')
    return HttpResponse(template.render({'unhealthy_products': unhealthy_products}, request=request))



    # L'utilisateur clique sur un des produits non sains
    # Le système affiche le meilleur substitut
