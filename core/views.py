# ==========================================
# MyCarMarket Australia
# Version: v2.2.13
# File: core/views.py
# Location: core/views.py
# Description:
# Homepage and custom error page views.
# Displays featured vehicles, latest vehicles,
# latest car reviews and latest approved car services.
# Featured and latest homepage sections show
# a maximum of 5 records each.
# Last Updated: 18 Jul 2026
# ==========================================

from django.shortcuts import render

from core.models import SiteSettings

from vehicles.models import (
    Car,
    FavouriteCar,
)

from reviews.models import CarReview

from services.models import CarService


# ==========================================
# SECTION 01 START
# HOME PAGE
# ==========================================

def home(request):

    approved_cars = Car.objects.filter(
        is_approved=True,
        is_active=True,
        moderation_status='approved',
    )

    featured_cars = approved_cars.filter(
        is_featured=True,
    ).order_by(
        '-is_verified_listing',
        '-created_at',
    )[:5]

    latest_cars = approved_cars.order_by(
        '-is_featured',
        '-is_verified_listing',
        '-created_at',
    )[:5]

    latest_reviews = CarReview.objects.filter(
        is_published=True,
    ).order_by(
        '-is_featured',
        '-published_at',
    )[:5]

    latest_services = CarService.objects.filter(
        is_active=True,
        is_approved=True,
        moderation_status='approved',
    ).order_by(
        '-is_featured',
        '-created_at',
    )[:5]

    favourite_car_ids = []

    if request.user.is_authenticated:

        favourite_car_ids = list(
            FavouriteCar.objects.filter(
                user=request.user,
            ).values_list(
                'car_id',
                flat=True,
            )
        )

    settings = SiteSettings.objects.first()

    return render(
        request,
        'core/home.html',
        {
            'featured_cars': featured_cars,
            'latest_cars': latest_cars,
            'latest_reviews': latest_reviews,
            'latest_services': latest_services,
            'favourite_car_ids': favourite_car_ids,
            'settings': settings,
        },
    )


# ==========================================
# SECTION 01 END
# HOME PAGE
# ==========================================


# ==========================================
# SECTION 02 START
# SELL CAR PAGE
# ==========================================

def sell_car(request):

    return render(
        request,
        'core/sell_car.html',
    )


# ==========================================
# SECTION 02 END
# SELL CAR PAGE
# ==========================================


# ==========================================
# SECTION 03 START
# DEALERS PAGE
# ==========================================

def dealers(request):

    return render(
        request,
        'core/dealers.html',
    )


# ==========================================
# SECTION 03 END
# DEALERS PAGE
# ==========================================


# ==========================================
# SECTION 04 START
# TERMS AND CONDITIONS
# ==========================================

def terms_conditions(request):

    return render(
        request,
        'core/terms_conditions.html',
    )


# ==========================================
# SECTION 04 END
# TERMS AND CONDITIONS
# ==========================================


# ==========================================
# SECTION 05 START
# PRIVACY POLICY
# ==========================================

def privacy_policy(request):

    return render(
        request,
        'core/privacy_policy.html',
    )


# ==========================================
# SECTION 05 END
# PRIVACY POLICY
# ==========================================


# ==========================================
# SECTION 06 START
# CONTACT US
# ==========================================

def contact_us(request):

    return render(
        request,
        'core/contact_us.html',
    )


# ==========================================
# SECTION 06 END
# CONTACT US
# ==========================================


# ==========================================
# SECTION 07 START
# CUSTOM ERROR PAGES
# ==========================================

def custom_403(request, exception=None):

    return render(
        request,
        'errors/403.html',
        status=403,
    )


def custom_404(request, exception=None):

    return render(
        request,
        'errors/404.html',
        status=404,
    )


def custom_500(request):

    return render(
        request,
        'errors/500.html',
        status=500,
    )


# ==========================================
# SECTION 07 END
# CUSTOM ERROR PAGES
# ==========================================


# ==========================================
# END CORE VIEWS
# ==========================================