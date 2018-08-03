from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def home(request):
    template = loader.get_template('healthier_food/home.html')
    return HttpResponse(template.render(request=request))
