# ==========================================
# MyCarMarket
# Version: v0.6.7
# File: vehicles/urls.py
# SEO Friendly Car URLs
# ==========================================

from django.urls import path
from . import views

urlpatterns = [

    # Car Listings
    path('', views.car_list, name='car_list'),

    # SEO Friendly Car URL
    path(
        'car/<slug:slug>/',
        views.car_detail,
        name='car_detail'
    ),

    # Dealer Profile
    path(
        'dealer/<int:user_id>/',
        views.dealer_detail,
        name='dealer_detail'
    ),

    # Create Listing
    path(
        'create/',
        views.create_car,
        name='create_car'
    ),

    # Seller Dashboard
    path(
        'my-listings/',
        views.my_listings,
        name='my_listings'
    ),

    # Edit Listing
    path(
        'edit/<int:pk>/',
        views.edit_car,
        name='edit_car'
    ),

    # Delete Listing
    path(
        'delete/<int:pk>/',
        views.delete_car,
        name='delete_car'
    ),
]