# ==========================================
# MyCarMarket
# Version: v0.9.5
# File: vehicles/urls.py
# SEO URLs + Favourite Cars + Dealer Packages
# ==========================================

from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.car_list,
        name='car_list'
    ),

    path(
        'car/<slug:slug>/',
        views.car_detail,
        name='car_detail'
    ),

    path(
        'car/<slug:slug>/favourite/',
        views.toggle_favourite,
        name='toggle_favourite'
    ),

    path(
        'saved-cars/',
        views.saved_cars,
        name='saved_cars'
    ),

    path(
        'dealer/<str:username>/',
        views.dealer_detail,
        name='dealer_detail'
    ),

    # NEW v0.8.4
    path(
        'dealer-packages/',
        views.dealer_packages,
        name='dealer_packages'
    ),

    path(
        'create/',
        views.create_car,
        name='create_car'
    ),

    path(
        'my-listings/',
        views.my_listings,
        name='my_listings'
    ),

    path(
        'edit/<int:pk>/',
        views.edit_car,
        name='edit_car'
    ),

    path(
        'delete/<int:pk>/',
        views.delete_car,
        name='delete_car'
    ),
]