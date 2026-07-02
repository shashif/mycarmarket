# ==========================================
# MyCarMarket
# Version: v1.6.9
# File: core/urls.py
# Description: Home + Dealers + SEO Friendly Legal Pages + Contact
# ==========================================

from django.urls import path

from .views import (
    home,
    sell_car,
    dealers,
    terms_conditions,
    privacy_policy,
    contact_us,
)

urlpatterns = [

    # ==========================================
    # HOME
    # ==========================================
    path(
        '',
        home,
        name='home'
    ),

    # ==========================================
    # SELL CAR
    # ==========================================
    path(
        'sell-car/',
        sell_car,
        name='sell_car'
    ),

    # ==========================================
    # DEALERS
    # ==========================================
    path(
        'dealers/',
        dealers,
        name='dealers'
    ),

    # ==========================================
    # LEGAL PAGES (SEO FRIENDLY)
    # ==========================================
    path(
        'terms/',
        terms_conditions,
        name='terms_conditions'
    ),

    path(
        'privacy/',
        privacy_policy,
        name='privacy_policy'
    ),

    path(
        'contact/',
        contact_us,
        name='contact_us'
    ),

]