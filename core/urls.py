# ==========================================
# MyCarMarket
# Version: v1.0.0 Launch Candidate
# File: core/urls.py
# Home + Dealers + Legal Pages + Contact
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
    path('', home, name='home'),

    path('sell-car/', sell_car, name='sell_car'),

    path('dealers/', dealers, name='dealers'),

    # Legal Pages
    path(
        'terms-and-conditions/',
        terms_conditions,
        name='terms_conditions'
    ),

    path(
        'privacy-policy/',
        privacy_policy,
        name='privacy_policy'
    ),

    path(
        'contact-us/',
        contact_us,
        name='contact_us'
    ),
]