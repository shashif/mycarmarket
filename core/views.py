# ==========================================
# MyCarMarket
# Version: v1.0.0 Launch Candidate
# File: core/views.py
# Homepage + Legal Pages + Contact + Custom 404
# ==========================================

from django.shortcuts import render
from core.models import SiteSettings
from vehicles.models import Car


# ==========================================
# HOME PAGE
# ==========================================

def home(request):
    featured_cars = Car.objects.filter(
        is_approved=True,
        is_featured=True
    ).order_by('-created_at')[:3]

    latest_cars = Car.objects.filter(
        is_approved=True
    ).order_by('-created_at')[:6]

    settings = SiteSettings.objects.first()

    return render(
        request,
        'core/home.html',
        {
            'featured_cars': featured_cars,
            'latest_cars': latest_cars,
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
# CUSTOM 404 PAGE
# ==========================================

def custom_404(request, exception):
    return render(
        request,
        '404.html',
        status=404
    )