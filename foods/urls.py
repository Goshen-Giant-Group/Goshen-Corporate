"""URL configuration for Goshen Giant Food Limited / Naturis Marketplace."""

from django.urls import path, re_path
from . import views

app_name = 'foods'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^about/?$', views.about, name='about'),
    re_path(r'^trade-terms/?$', views.trade_terms, name='trade_terms'),
    re_path(r'^privacy/?$', views.privacy, name='privacy'),
    re_path(r'^contact/?$', views.contact, name='contact'),
    re_path(r'^products/(?P<product_id>[a-zA-Z0-9_-]+)/?$', views.product_detail, name='product_detail'),
    re_path(r'^api/fx/?$', views.api_fx, name='api_fx'),
    re_path(r'^api/quote/?$', views.api_quote, name='api_quote'),
]
