# ==========================================
# MyCarMarket
# Version: v0.3.1 - Dealers Page
# File: core/views.py
# ==========================================

from django.shortcuts import render
from vehicles.models import Car


def home(request):
    featured_cars = Car.objects.filter(is_featured=True).order_by('-created_at')[:3]
    latest_cars = Car.objects.all().order_by('-created_at')[:6]

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