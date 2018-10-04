#! /usr/bin/env python3
# coding: utf-8

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Product, Category, Favorite
from .forms import NewAccountForm, LoginForm
from .params import max_products


def home(request):
    return render(request, 'healthier_food/pages/home.html')


def search(request):

    # Query submitted by user
    query = request.POST.get('query')

    if not query:
        context = {}

    else:
        unhealthy_products_list = []

        # Get unhealthy products (i.e. nutriscore = D ou E) which name contains user query
        unhealthy_products = Product.objects.filter((Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query)) & (Q(nutriscore="D") | Q(nutriscore="E")))[:max_products]
        for unhealthy_product in unhealthy_products:
            unhealthy_products_list.append(unhealthy_product)

        products = paginate(request, unhealthy_products_list, 6)

        context = {
            'query': query,
            'products': products
        }

    return render(request, 'healthier_food/pages/search.html', context)


def substitute(request, unhealthy_product_code):
    """ Select a list of healthy products sharing a maximum of categories with submitted unhealthy one """

    # Unhealthy product submitted by user
    unhealthy_product = get_object_or_404(Product, code=unhealthy_product_code)

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
            if get_object_or_404(Category, name=category) in healthy_product_categories:
                shared_categories.append(category)

        # Make a correspondance between healthy product & number of shared categories
        shared_categories_counter[healthy_product] = len(shared_categories)

    try:
        # Get maximum number of shared categories
        maximum = max(shared_categories_counter.values())

        # Make a list of healthy products sharing the maximum number of categories with unhealthy product
        best_matches = []
        for healthy_product, number_of_shared_categories in shared_categories_counter.items():
            if number_of_shared_categories == maximum and len(best_matches) < max_products:
                best_matches.append(healthy_product)

        # Rearrange 'best_matches' list (putting "A"-products first)
        healthiest_first_list = []
        for match in best_matches:
            if match.nutriscore == "A":
                healthiest_first_list.append(match)
        for match in best_matches:
            if match.nutriscore == "B":
                healthiest_first_list.append(match)

        products = paginate(request, healthiest_first_list, 6)

    # If 'counter' is empty (i.e. no healthy product shares at least one category with unhealthy product)
    except ValueError as e:
        # Healthy products list is empty
        products = []

    context = {
        'unhealthy_product': unhealthy_product,
        'products': products
    }

    return render(request, 'healthier_food/pages/substitute.html', context)


def details(request, product_code):
    product = get_object_or_404(Product, code=product_code)

    # context = {
    #     'product': product
    # }

    return render(request, 'healthier_food/pages/details.html', locals())


def new_account(request):
    form = NewAccountForm()

    # context = {
    #     'form': form
    # }

    return render(request, 'healthier_food/pages/new_account.html', locals())


def account_creation(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('email')
    email = request.POST.get('email')
    password = request.POST.get('password')

    contact = User.objects.filter(username=username)

    if not contact.exists():
        contact = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

        # context = {
        #     'contact': contact,
        # }

        return render(request, 'healthier_food/pages/account_success.html', locals())

    else:
        context = {
            'contact': contact[0],
        }

        return render(request, 'healthier_food/pages/account_failure.html', context)


def login_user(request):
    error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data[('username')]
            password = form.cleaned_data[('password')]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                error = True
    else:
        form = LoginForm()

    return render(request, 'healthier_food/pages/login.html', locals())


def my_account(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    # contact = authenticate(username=username, password=password)
    contact = authenticate(username='Toto')
    # contact = {'username': 'Toto'}

    if contact:
        login(contact)

        context = {
            'contact': contact
        }

        return render(request, 'healthier_food/pages/my_account.html', context)

    else:
        return render(request, 'healthier_food/pages/login_failure.html')


def favorites(request):
    favorites = Favorite.objects.all()


    context = {
        'favorites': favorites
    }

    return render(request, 'healthier_food/pages/favorites.html', context)


def add_favorite(request, favorite_code):
    username = "Toto"

    # Check if favorite already in DB
    favorite = Favorite.objects.filter(code=favorite_code)

    if not favorite.exists():
        product = get_object_or_404(Product, code=favorite_code)
        favorite = Favorite.objects.create(username=username,
                                           code=product.code,
                                           name=product.name,
                                           description=product.description,
                                           url=product.url,
                                           nutriscore=product.nutriscore,
                                           image=product.image
                                           )

        # context = {
        #     'favorite': favorite
        # }

        return render(request, 'healthier_food/pages/favorite_success.html', locals())


def logout_user(request):
    logout(request)
    return render(request, 'healthier_food/pages/logout.html')


def paginate(request, product_list, nb):
    """ Not a view but a function to factorise pagination code """
    paginator = Paginator(product_list, nb)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return products
