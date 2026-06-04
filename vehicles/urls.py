# ==========================================
# MyCarMarket
# Version: v0.3.2 - Fixed Detail URL
# File: vehicles/urls.py
# ==========================================

from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('<int:car_id>/', views.car_detail, name='car_detail'),
]