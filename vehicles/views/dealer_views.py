# ==========================================
# MyCarMarket
# Version: v0.6.8
# File: vehicles/views/dealer_views.py
# Dealer Public Profile View
# ==========================================

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from vehicles.models import Car


def dealer_detail(request, user_id):
    dealer = get_object_or_404(User, id=user_id)

    cars = Car.objects.filter(
        seller=dealer,
        is_approved=True
    ).order_by('-created_at')

    share_url = request.build_absolute_uri()
    share_text = f"Check out this dealer on MyCarMarket Australia: {dealer.username}"

    return render(
        request,
        'vehicles/dealer_detail.html',
        {
            'dealer': dealer,
            'cars': cars,
            'share_url': share_url,
            'share_text': share_text,
        }
    )