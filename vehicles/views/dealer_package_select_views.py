# ==========================================
# MyCarMarket
# Version: v1.1.2
# File: vehicles/views/dealer_package_select_views.py
# Dealer Package Payment Select Page
# ==========================================

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dealer_package_select(request):

    packages = [
        {
            "name": "Free",
            "slug": "free",
            "price": 0,
            "badge": "",
            "features": [
                "3 car listings",
                "No featured ads",
                "No verified badge",
                "Basic seller profile",
                "Standard search listing",
            ],
        },
        {
            "name": "Starter",
            "slug": "starter",
            "price": 99,
            "badge": "",
            "features": [
                "10 car listings",
                "1 featured ad",
                "Starter dealer badge",
                "Better listing visibility",
                "Dealer profile page",
            ],
        },
        {
            "name": "Professional",
            "slug": "professional",
            "price": 299,
            "badge": "Most Popular",
            "features": [
                "30 car listings",
                "5 featured ads",
                "Verified dealer badge",
                "Higher search visibility",
                "Priority dealer exposure",
            ],
        },
        {
            "name": "Premium",
            "slug": "premium",
            "price": 599,
            "badge": "",
            "features": [
                "75 car listings",
                "15 featured ads",
                "Premium dealer badge",
                "Strong search boost",
                "Homepage dealer exposure",
            ],
        },
        {
            "name": "Enterprise",
            "slug": "enterprise",
            "price": 999,
            "badge": "",
            "features": [
                "Unlimited listings",
                "30 featured ads",
                "Enterprise dealer badge",
                "Maximum search exposure",
                "Priority support",
            ],
        },
    ]

    return render(
        request,
        "vehicles/dealer_package_select.html",
        {
            "packages": packages
        }
    )