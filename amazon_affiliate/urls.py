# ==========================================
# MyCarMarket
# Version: v1.15.1
# File: amazon_affiliate/urls.py
# Description:
# Amazon Accessories Store URLs
# Product List + Click Tracking Redirect
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

    path(
        "accessories/go/<int:product_id>/",
        views.amazon_product_redirect,
        name="amazon_product_redirect"
    ),
]