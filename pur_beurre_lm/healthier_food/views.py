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
