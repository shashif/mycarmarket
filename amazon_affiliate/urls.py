# ==========================================
# MyCarMarket
# Version: v1.14.0
# File: amazon_affiliate/urls.py
# Description: Amazon Accessories Store URLs
# ==========================================

from django.urls import path

from . import views


urlpatterns = [
    path(
        "accessories/",
        views.amazon_product_list,
        name="amazon_product_list"
    ),
    path(
        "accessories/<slug:category_slug>/",
        views.amazon_product_list,
        name="amazon_product_category"
    ),
]