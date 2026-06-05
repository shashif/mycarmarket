# ==========================================
# MyCarMarket
# Version: v0.4.0
# File: vehicles/urls.py
# ==========================================

from django.urls import path
from . import views


urlpatterns = [
    path('', views.car_list, name='car_list'),

    path('car/<int:pk>/', views.car_detail, name='car_detail'),

    path('create/', views.create_car, name='create_car'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('edit/<int:pk>/', views.edit_car, name='edit_car'),
    path('delete/<int:pk>/', views.delete_car, name='delete_car'),
]