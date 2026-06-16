# ==========================================
# MyCarMarket
# Version: v1.2.0
# File: vehicles/views/dealer_dashboard_views.py
# Dealer Dashboard
# ==========================================

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from vehicles.models import Car, Enquiry


@login_required
def dealer_dashboard(request):

    cars = Car.objects.filter(
        seller=request.user
    ).order_by('-created_at')

    total_listings = cars.count()
    active_listings = cars.filter(is_active=True).count()
    approved_listings = cars.filter(is_approved=True).count()
    pending_listings = cars.filter(is_approved=False).count()
    featured_listings = cars.filter(is_featured=True).count()

    total_views = sum(car.views_count for car in cars)

    total_enquiries = Enquiry.objects.filter(
        car__seller=request.user
    ).count()

    recent_enquiries = Enquiry.objects.filter(
        car__seller=request.user
    ).select_related('car').order_by('-created_at')[:5]

    top_cars = cars.order_by('-views_count')[:5]

    dealer_profile = None

    if hasattr(request.user, 'dealer_profile'):
        dealer_profile = request.user.dealer_profile

    package_name = 'Free'
    package_active = False
    package_expiry = None
    listing_limit = 1
    featured_limit = 0

    if dealer_profile:
        package_name = dealer_profile.package
        package_active = dealer_profile.package_active
        package_expiry = dealer_profile.package_expiry
        listing_limit = dealer_profile.max_listings
        featured_limit = dealer_profile.featured_ads_allowed

    return render(
        request,
        'vehicles/dealer_dashboard.html',
        {
            'cars': cars,
            'dealer_profile': dealer_profile,
            'total_listings': total_listings,
            'active_listings': active_listings,
            'approved_listings': approved_listings,
            'pending_listings': pending_listings,
            'featured_listings': featured_listings,
            'total_views': total_views,
            'total_enquiries': total_enquiries,
            'recent_enquiries': recent_enquiries,
            'top_cars': top_cars,
            'package_name': package_name,
            'package_active': package_active,
            'package_expiry': package_expiry,
            'listing_limit': listing_limit,
            'featured_limit': featured_limit,
        }
    )


# ==========================================
# END DEALER DASHBOARD
# ==========================================