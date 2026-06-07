# ==========================================
# MyCarMarket
# Version: v0.5.2
# File: core/views.py
# Homepage Shows Approved Listings Only
# ==========================================

from django.shortcuts import render
from vehicles.models import Car


def home(request):
    featured_cars = Car.objects.filter(
        is_approved=True,
        is_featured=True
    ).order_by('-created_at')[:3]

    latest_cars = Car.objects.filter(
        is_approved=True
    ).order_by('-created_at')[:6]

    return render(
        request,
        'core/home.html',
        {
            'featured_cars': featured_cars,
            'latest_cars': latest_cars,
        }
    )


def sell_car(request):
    return render(request, 'core/sell_car.html')


def dealers(request):
    return render(request, 'core/dealers.html')