# ==========================================
# MyCarMarket
# Version: v0.8.8
# File: vehicles/views/dealer_views.py
# Dealer Public Profile with Branding + Share
# ==========================================

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from vehicles.models import Car


def dealer_detail(request, username):
    dealer = get_object_or_404(User, username=username)

    dealer_profile = None

    if hasattr(dealer, 'dealer_profile'):
        dealer_profile = dealer.dealer_profile

    cars = Car.objects.filter(
        seller=dealer,
        is_approved=True,
        is_active=True
    ).order_by('-created_at')

    business_name = dealer.username

    if dealer_profile and dealer_profile.business_name:
        business_name = dealer_profile.business_name

    share_url = request.build_absolute_uri()
    share_text = f"Check out {business_name} on MyCarMarket Australia"

    return render(
        request,
        'vehicles/dealer_detail.html',
        {
            'dealer': dealer,
            'dealer_profile': dealer_profile,
            'cars': cars,
            'business_name': business_name,
            'share_url': share_url,
            'share_text': share_text,
        }
    )