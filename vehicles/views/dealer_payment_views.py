# ==========================================
# MyCarMarket
# Version: v1.1.2
# File: vehicles/views/dealer_payment_views.py
# Dealer Package Payment Select Page
# ==========================================

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dealer_package_select(request):
    packages = [
        {
            "name": "Free",
            "price": 0,
            "ads": 2,
            "featured": 0,
            "badge": "Basic Listing",
        },
        {
            "name": "Basic",
            "price": 49,
            "ads": 10,
            "featured": 2,
            "badge": "Dealer Badge",
        },
        {
            "name": "Premium",
            "price": 99,
            "ads": 30,
            "featured": 8,
            "badge": "Verified Dealer",
        },
        {
            "name": "Enterprise",
            "price": 199,
            "ads": 100,
            "featured": 25,
            "badge": "Priority Dealer",
        },
    ]

    return render(request, "vehicles/dealer_package_select.html", {
        "packages": packages
    })