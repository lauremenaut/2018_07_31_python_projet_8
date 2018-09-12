#! /usr/bin/env python3
# coding: utf-8

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

from .models import Product, Category, Favorite


def home(request):
    return render(request, 'pages/home.html')


def search(request):

    # Query submitted by user
    query = request.GET.get('query')

    unhealthy_products_list = []

    # Get unhealthy products (i.e. nutriscore = D ou E) which name contains user query
    unhealthy_products = Product.objects.filter(name__icontains=query).exclude(nutriscore="A").exclude(nutriscore="B")[:6]
    for unhealthy_product in unhealthy_products:
        unhealthy_products_list.append(unhealthy_product)

    # If less than 6 'found by name' products, then add 'found by desription' products
    if len(unhealthy_products_list) < 6:
        more_unhealthy_products = Product.objects.filter(description__icontains=query).exclude(nutriscore="A").exclude(nutriscore="B")[:6]

        try:
            i = 0
            while len(unhealthy_products_list) < 6:
                # Add product only if not already in the list
                if more_unhealthy_products[i] not in unhealthy_products_list:
                    unhealthy_products_list.append(more_unhealthy_products[i])
                i += 1
        except IndexError:
            pass

    # If still less than 6 products, then add 'found by brand' products
    if len(unhealthy_products_list) < 6:
        more_unhealthy_products = Product.objects.filter(brand__icontains=query).exclude(nutriscore="A").exclude(nutriscore="B")[:6]

        try:
            i = 0
            while len(unhealthy_products_list) < 6:
                # Add product only if not already in the list
                if more_unhealthy_products[i] not in unhealthy_products_list:
                    unhealthy_products_list.append(more_unhealthy_products[i])
                i += 1
        except IndexError:
            pass

    context = {
        'unhealthy_products': unhealthy_products_list
    }

    return render(request, 'pages/search.html', context)


def substitute(request, unhealthy_product_code):
    """ Select a list of healthy products sharing a maximum of categories with submitted unhealthy one """

    # Unhealthy product submitted by user
    unhealthy_product = Product.objects.get(code=unhealthy_product_code)

    # Get healthy products sharing at least one category with unhealthy product
    healthy_products_list = []
    categories = unhealthy_product.categories.all()
    for category in categories:
        healthy_products = Product.objects.filter(categories=category).exclude(nutriscore="D").exclude(nutriscore="E")
        for healthy_product in healthy_products:
            if healthy_product not in healthy_products_list:
                healthy_products_list.append(healthy_product)

    # Count shared categories between healthy and unhealthy products
    shared_categories_counter = {}
    for healthy_product in healthy_products_list:
        shared_categories = []
        healthy_product_categories = healthy_product.categories.all()

        # Add shared categories in 'shared_categories' list
        for category in categories:
            if Category.objects.get(name=category) in healthy_product_categories:
                shared_categories.append(category)

        # Make a correspondance between healthy product & number of shared categories
        shared_categories_counter[healthy_product] = len(shared_categories)

    try:
        # Get maximum number of shared categories
        maximum = max(shared_categories_counter.values())

    # If 'counter' is empty (i.e. no healthy product shares at least one category with unhealthy product)
    except ValueError as e:
        # Healthy products list is empty
        healthiest_matches_list = []

    # Make a list of healthy products sharing the maximum number of categories with unhealthy product
    best_matches = []
    for healthy_product, number_of_shared_categories in shared_categories_counter.items():
        if number_of_shared_categories == maximum and len(best_matches) < 6:
            best_matches.append(healthy_product)

    # Make a sub-list of healthiest products (nutriscore = A)
    healthiest_matches_list = []
    for match in best_matches:
            healthiest_matches = Product.objects.filter(name=match).filter(nutriscore="A")[:6]
            for healthiest_match in healthiest_matches:
                healthiest_matches_list.append(healthiest_match)

    # If number of healthiest products < 6 and more 'best matches' left then add 'best match' to list
    i = 0
    while len(healthiest_matches_list) < 6 and len(healthiest_matches_list) < len(best_matches):
        if best_matches[i] not in healthiest_matches_list:
            healthiest_matches_list.append(best_matches[i])
        i += 1

    context = {
        'unhealthy_product': unhealthy_product,
        'healthy_products': healthiest_matches_list
    }

    return render(request, 'pages/substitute.html', context)


def details(request, product_code):
    code = int(product_code)
    product = Product.objects.get(code=code)

    context = {
        'product': product
    }

    return render(request, 'pages/details.html', context)


def new_account(request):
    return render(request, 'pages/new_account.html')


def account_creation(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    contact = User.objects.filter(username=username)
    contact = {'username': 'Toto', 'password': 'h6ufd7iu'}

    if not contact:
        # contact = User.objects.create_user(username=username, email=email, password=password)


        context = {
            'contact': contact
        }

        return render(request, 'pages/account_success.html', context)

    else:
        return render(request, 'pages/account_failure.html')


def login_user(request):
    return render(request, 'pages/login.html')


def my_account(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    # contact = authenticate(username=username, password=password)
    contact = authenticate(username='Toto')
    # contact = {'username': 'Toto'}

    if contact:
        login(contact)

        context = {
            'contact': contact
        }

        return render(request, 'pages/my_account.html', context)

    else:
        return render(request, 'pages/login_failure.html')


def favorites(request):
    favorites = Favorite.objects.all()


    context = {
        'favorites': favorites
    }

    return render(request, 'pages/favorites.html', context)


def add_favorite(request, favorite_code):
    username = "Toto"

    product = Product.objects.get(code=favorite_code)

    favorite = Favorite.objects.create(username=username,
                                       code=product.code,
                                       name=product.name,
                                       description=product.description,
                                       url=product.url,
                                       nutriscore=product.nutriscore,
                                       image=product.image
                                       )

    context = {
        'favorite': favorite
    }

    return render(request, 'pages/favorite_success.html', context)


def logout_user(request):
    logout(request)
    return render(request, 'pages/logout.html')
