from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^search/$', views.search),
    re_path(r'^substitute/(?P<unhealthy_product_code>[0-9]+)$', views.substitute),
    re_path(r'^(?P<product_code>[0-9]+)$', views.detail),
]
