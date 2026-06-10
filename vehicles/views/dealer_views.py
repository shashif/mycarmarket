# ==========================================
# MyCarMarket
# Version: v0.9.3
# File: vehicles/views/dealer_views.py
# Premium Dealer Profile + Dealer Trust Centre
# ==========================================

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

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

    featured_cars = cars.filter(
        is_featured=True
    )[:3]

    total_cars = cars.count()
    total_views = sum(car.views_count for car in cars)
    total_enquiries = sum(car.enquiries.count() for car in cars)

    member_since = dealer.date_joined.year

    years_active = timezone.now().year - dealer.date_joined.year

    if years_active < 1:
        years_active = 1

    trust_score = (
        total_cars * 2 +
        total_views // 20 +
        total_enquiries * 5 +
        years_active * 3
    )

    if dealer_profile and dealer_profile.is_verified:
        trust_score += 20

    if dealer_profile and dealer_profile.is_featured_dealer:
        trust_score += 10

    if trust_score > 100:
        trust_score = 100

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
            'featured_cars': featured_cars,
            'total_cars': total_cars,
            'total_views': total_views,
            'total_enquiries': total_enquiries,
            'member_since': member_since,
            'years_active': years_active,
            'trust_score': trust_score,
            'business_name': business_name,
            'share_url': share_url,
            'share_text': share_text,
        }
    )