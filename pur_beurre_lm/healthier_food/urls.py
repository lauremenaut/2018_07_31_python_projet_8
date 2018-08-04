from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<product_code>[0-9]+)$', views.detail),
    re_path(r'^search/$', views.search),
]
