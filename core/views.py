# ==========================================
# MyCarMarket Australia
# Version: v2.3.0
# File: core/views.py
# Location: core/views.py
# Description:
# - Homepage and custom error page views
# - Unified staff-only moderation center
# - Pending Cars, Rentals and Services
# - One-click approve and reject actions
# - Preserves vehicle approval/rejection emails
# - No database migration required
# Last Updated: 24 Jul 2026
# ==========================================

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.models import SiteSettings

from vehicles.models import (
    Car,
    FavouriteCar,
)

from vehicles.utils.email_notifications import (
    send_listing_approved_email,
    send_listing_rejected_email,
)

from rentals.models import RentalCar
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
# UNIFIED MODERATION CENTER
# ==========================================

@staff_member_required
def moderation_center(request):

    pending_cars = Car.objects.filter(
        moderation_status='pending',
    ).order_by(
        '-created_at',
    )

    pending_rentals = RentalCar.objects.filter(
        moderation_status='pending',
    ).order_by(
        '-created_at',
    )

    pending_services = CarService.objects.filter(
        moderation_status='pending',
    ).order_by(
        '-created_at',
    )

    car_count = pending_cars.count()
    rental_count = pending_rentals.count()
    service_count = pending_services.count()

    return render(
        request,
        'core/moderation_center.html',
        {
            'pending_cars': pending_cars,
            'pending_rentals': pending_rentals,
            'pending_services': pending_services,
            'car_count': car_count,
            'rental_count': rental_count,
            'service_count': service_count,
            'total_pending_count': (
                car_count
                + rental_count
                + service_count
            ),
        },
    )


@staff_member_required
@require_POST
def moderation_action(request, listing_type, object_id, action):

    model_map = {
        'car': Car,
        'rental': RentalCar,
        'service': CarService,
    }

    model = model_map.get(listing_type)

    if model is None:
        raise Http404('Invalid listing type.')

    listing = get_object_or_404(
        model,
        pk=object_id,
    )

    if action == 'approve':

        old_status = listing.moderation_status

        listing.moderation_status = 'approved'
        listing.is_approved = True
        listing.is_active = True

        update_fields = [
            'moderation_status',
            'is_approved',
            'is_active',
        ]

        if isinstance(listing, Car):
            listing.approved_by = request.user
            listing.approved_at = timezone.now()

            update_fields.extend([
                'approved_by',
                'approved_at',
            ])

        listing.save(
            update_fields=update_fields,
        )

        if isinstance(listing, Car) and old_status != 'approved':
            send_listing_approved_email(listing)

        messages.success(
            request,
            f'{listing.title} approved successfully.',
        )

    elif action == 'reject':

        old_status = listing.moderation_status

        listing.moderation_status = 'rejected'
        listing.is_approved = False
        listing.is_active = False

        listing.save(
            update_fields=[
                'moderation_status',
                'is_approved',
                'is_active',
            ],
        )

        if isinstance(listing, Car) and old_status != 'rejected':
            send_listing_rejected_email(listing)

        messages.warning(
            request,
            f'{listing.title} rejected successfully.',
        )

    else:
        raise Http404('Invalid moderation action.')

    return redirect(
        'moderation_center',
    )


# ==========================================
# SECTION 07 END
# UNIFIED MODERATION CENTER
# ==========================================


# ==========================================
# SECTION 08 START
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
# SECTION 08 END
# CUSTOM ERROR PAGES
# ==========================================


# ==========================================
# END CORE VIEWS
# ==========================================
