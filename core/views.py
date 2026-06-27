# ==========================================
# MyCarMarket
# Version: v1.6.0
# File: core/views.py
# Description: Homepage + Custom Error Pages
# ==========================================

import random

from django.shortcuts import render

from core.models import SiteSettings

from vehicles.models import (
    Car,
    FavouriteCar
)


# ==========================================
# HOME PAGE
# ==========================================

def home(request):

    featured_queryset = Car.objects.filter(
        is_approved=True,
        is_active=True,
        is_featured=True
    ).order_by(
        '-is_verified_listing',
        '-created_at'
    )

    featured_car_ids = list(
        featured_queryset.values_list(
            'id',
            flat=True
        )
    )

    if 'home_featured_car_ids' not in request.session:

        random.shuffle(featured_car_ids)

        request.session['home_featured_car_ids'] = featured_car_ids[:12]

    session_featured_ids = request.session.get(
        'home_featured_car_ids',
        []
    )

    featured_cars = Car.objects.filter(
        id__in=session_featured_ids,
        is_approved=True,
        is_active=True,
        is_featured=True
    )

    latest_cars = Car.objects.filter(
        is_approved=True,
        is_active=True
    ).order_by(
        '-is_featured',
        '-is_verified_listing',
        '-created_at'
    )[:6]

    favourite_car_ids = []

    if request.user.is_authenticated:

        favourite_car_ids = list(
            FavouriteCar.objects.filter(
                user=request.user
            ).values_list(
                'car_id',
                flat=True
            )
        )

    settings = SiteSettings.objects.first()

    return render(
        request,
        'core/home.html',
        {
            'featured_cars': featured_cars,
            'latest_cars': latest_cars,
            'favourite_car_ids': favourite_car_ids,
            'settings': settings,
        }
    )


# ==========================================
# SELL CAR PAGE
# ==========================================

def sell_car(request):

    return render(
        request,
        'core/sell_car.html'
    )


# ==========================================
# DEALERS PAGE
# ==========================================

def dealers(request):

    return render(
        request,
        'core/dealers.html'
    )


# ==========================================
# TERMS & CONDITIONS
# ==========================================

def terms_conditions(request):

    return render(
        request,
        'core/terms_conditions.html'
    )


# ==========================================
# PRIVACY POLICY
# ==========================================

def privacy_policy(request):

    return render(
        request,
        'core/privacy_policy.html'
    )


# ==========================================
# CONTACT US
# ==========================================

def contact_us(request):

    return render(
        request,
        'core/contact_us.html'
    )


# ==========================================
# CUSTOM ERROR PAGES
# ==========================================

def custom_403(request, exception=None):

    return render(
        request,
        'errors/403.html',
        status=403
    )


def custom_404(request, exception=None):

    return render(
        request,
        'errors/404.html',
        status=404
    )


def custom_500(request):

    return render(
        request,
        'errors/500.html',
        status=500
    )


# ==========================================
# END CORE VIEWS
# ==========================================