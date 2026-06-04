# ==========================================
# MyCarMarket
# Version: v0.3.1 - Dealers Page
# File: core/urls.py
# ==========================================

from django.urls import path
from .views import home, sell_car, dealers

urlpatterns = [
    path('', home, name='home'),
    path('sell-car/', sell_car, name='sell_car'),
    path('dealers/', dealers, name='dealers'),
]