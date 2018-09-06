from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^search/$', views.search, name='search'),
    re_path(r'^substitute/(?P<unhealthy_product_code>[0-9]+)$', views.substitute, name='substitute'),
    re_path(r'^(?P<product_code>[0-9]+)$', views.detail, name='detail'),
]
