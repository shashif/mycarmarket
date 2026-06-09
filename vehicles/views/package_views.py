# ==========================================
# MyCarMarket
# Version: v0.8.4
# File: vehicles/views/package_views.py
# Dealer Packages Page
# ==========================================

from django.shortcuts import render


def dealer_packages(request):
    packages = [
        {
            'name': 'Free',
            'price': '0',
            'listings': '3 listings',
            'featured': '0 featured ads',
            'badge': 'Basic Seller',
        },
        {
            'name': 'Starter',
            'price': '99',
            'listings': '10 listings',
            'featured': '1 featured ad',
            'badge': 'Starter Dealer',
        },
        {
            'name': 'Professional',
            'price': '299',
            'listings': '30 listings',
            'featured': '5 featured ads',
            'badge': 'Professional Dealer',
        },
        {
            'name': 'Premium',
            'price': '599',
            'listings': '75 listings',
            'featured': '15 featured ads',
            'badge': 'Premium Dealer',
        },
        {
            'name': 'Enterprise',
            'price': '999',
            'listings': 'Unlimited listings',
            'featured': '30 featured ads',
            'badge': 'Enterprise Dealer',
        },
    ]

    return render(
        request,
        'vehicles/dealer_packages.html',
        {
            'packages': packages
        }
    )