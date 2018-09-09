from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^search/$', views.search, name='search'),
    re_path(r'^substitute/(?P<unhealthy_product_code>[0-9]+)$', views.substitute, name='substitute'),
    re_path(r'^detail/(?P<product_code>[0-9]+)$', views.detail, name='detail'),
    re_path(r'^new_account/$', views.new_account, name='new_account'),
    re_path(r'^success_account/$', views.success_account, name='success_account'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^my_account/$', views.my_account, name='my_account'),
]
