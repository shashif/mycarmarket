# ==========================================
# MyCarMarket
# Version: v0.9.0
# File: vehicles/views/dealer_views.py
# Premium Dealer Profile UI Data
# ==========================================

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from vehicles.models import Car


# ==========================================
# START SECTION 1: DEALER PUBLIC PROFILE VIEW
# ==========================================

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

    featured_cars = cars.filter(
        is_featured=True
    )[:3]

    total_cars = cars.count()

    business_name = dealer.username

    if dealer_profile and dealer_profile.business_name:
        business_name = dealer_profile.business_name

    member_since = dealer.date_joined.year

    share_url = request.build_absolute_uri()
    share_text = f"Check out {business_name} on MyCarMarket Australia"

    return render(
        request,
        'vehicles/dealer_detail.html',
        {
            'dealer': dealer,
            'dealer_profile': dealer_profile,
            'cars': cars,
            'featured_cars': featured_cars,
            'total_cars': total_cars,
            'business_name': business_name,
            'member_since': member_since,
            'share_url': share_url,
            'share_text': share_text,
        }
    )

# ==========================================
# END SECTION 1: DEALER PUBLIC PROFILE VIEW
# ==========================================