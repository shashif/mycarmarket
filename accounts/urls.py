# ==========================================
# MyCarMarket
# Version: v0.4.0
# File: accounts/urls.py
# ==========================================

from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
]