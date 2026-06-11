# ==========================================
# MyCarMarket
# Version: v0.9.7
# File: vehicles/views/car_manage_views.py
# Advanced Image Management + Featured Ad Limits + Dashboard Analytics
# ==========================================

from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from vehicles.models import Car, Enquiry
from vehicles.forms import CarForm


def user_is_dealer(user):
    return (
        hasattr(user, 'dealer_profile') and
        user.dealer_profile.is_dealer and
        user.dealer_profile.package_active
    )


def get_listing_limit(user):
    if not hasattr(user, 'dealer_profile'):
        return 1

    profile = user.dealer_profile

    if not profile.package_active:
        return 0

    if profile.package == 'enterprise':
        return None

    return profile.max_listings


def get_featured_limit(user):
    if user.is_staff:
        return None

    if not hasattr(user, 'dealer_profile'):
        return 1

    profile = user.dealer_profile

    if not profile.package_active:
        return 0

    if profile.package == 'enterprise':
        return None

    return profile.featured_ads_allowed


def get_featured_days(user):
    if not hasattr(user, 'dealer_profile'):
        return 7

    profile = user.dealer_profile

    if profile.package == 'starter':
        return 14

    if profile.package == 'professional':
        return 21

    if profile.package in ['premium', 'enterprise']:
        return 30

    return 7


def clean_expired_featured_ads():
    Car.objects.filter(
        is_featured=True,
        featured_until__isnull=False,
        featured_until__lt=timezone.now()
    ).update(
        is_featured=False,
        featured_until=None
    )


def user_can_create_listing(user):
    if user.is_staff:
        return True

    listing_limit = get_listing_limit(user)

    if listing_limit is None:
        return True

    current_count = Car.objects.filter(seller=user).count()

    return current_count < listing_limit


def user_can_feature_car(user, car=None):
    if user.is_staff:
        return True

    featured_limit = get_featured_limit(user)

    if featured_limit is None:
        return True

    featured_cars = Car.objects.filter(
        seller=user,
        is_featured=True
    )

    if car:
        featured_cars = featured_cars.exclude(pk=car.pk)

    return featured_cars.count() < featured_limit


@login_required
def create_car(request):
    clean_expired_featured_ads()

    if not user_can_create_listing(request.user):
        messages.error(
            request,
            'You have reached your package listing limit. Please upgrade your dealer package to add more cars.'
        )
        return redirect('my_listings')

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)

        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user

            if car.is_featured:
                if user_can_feature_car(request.user):
                    featured_days = get_featured_days(request.user)
                    car.featured_until = timezone.now() + timedelta(days=featured_days)
                else:
                    car.is_featured = False
                    car.featured_until = None
                    messages.error(
                        request,
                        'Featured ad limit reached for your package. Your car was saved as a normal listing.'
                    )

            if request.user.is_staff or user_is_dealer(request.user):
                car.is_approved = True
            else:
                car.is_approved = False

            car.save()

            images = request.FILES.getlist('images')

            for index, image in enumerate(images):
                car.images.create(
                    image=image,
                    is_primary=(index == 0),
                    sort_order=index
                )

            messages.success(request, 'Car listing saved successfully.')

            return redirect('car_detail', slug=car.slug)

    else:
        form = CarForm()

    return render(
        request,
        'vehicles/car_form.html',
        {
            'form': form
        }
    )


@login_required
def my_listings(request):
    clean_expired_featured_ads()

    cars = Car.objects.filter(
        seller=request.user
    ).order_by('-created_at')

    total_listings = cars.count()
    total_views = sum(car.views_count for car in cars)
    total_enquiries = sum(car.enquiries.count() for car in cars)

    approved_listings = cars.filter(is_approved=True).count()
    pending_listings = cars.filter(is_approved=False).count()
    active_listings = cars.filter(is_active=True).count()
    featured_listings = cars.filter(is_featured=True).count()

    listing_limit = get_listing_limit(request.user)
    featured_limit = get_featured_limit(request.user)

    if listing_limit is None:
        listings_remaining = 'Unlimited'
        listing_limit_display = 'Unlimited'
    else:
        listings_remaining = max(0, listing_limit - total_listings)
        listing_limit_display = listing_limit

    if featured_limit is None:
        featured_remaining = 'Unlimited'
        featured_limit_display = 'Unlimited'
    else:
        featured_remaining = max(0, featured_limit - featured_listings)
        featured_limit_display = featured_limit

    average_views = round(total_views / total_listings) if total_listings > 0 else 0

    top_performing_cars = cars.order_by('-views_count')[:5]

    recent_enquiries = Enquiry.objects.filter(
        car__seller=request.user
    ).select_related('car').order_by('-created_at')[:8]

    dealer_score = (
        total_listings * 5 +
        total_views +
        total_enquiries * 10 +
        featured_listings * 20
    )

    return render(
        request,
        'vehicles/my_listings.html',
        {
            'cars': cars,
            'total_listings': total_listings,
            'total_views': total_views,
            'total_enquiries': total_enquiries,
            'approved_listings': approved_listings,
            'pending_listings': pending_listings,
            'active_listings': active_listings,
            'featured_listings': featured_listings,
            'listing_limit': listing_limit_display,
            'listings_remaining': listings_remaining,
            'featured_limit': featured_limit_display,
            'featured_remaining': featured_remaining,
            'average_views': average_views,
            'top_performing_cars': top_performing_cars,
            'recent_enquiries': recent_enquiries,
            'dealer_score': dealer_score,
        }
    )


@login_required
def edit_car(request, pk):
    clean_expired_featured_ads()

    car = get_object_or_404(
        Car,
        pk=pk,
        seller=request.user
    )

    if request.method == 'POST':
        form = CarForm(
            request.POST,
            request.FILES,
            instance=car
        )

        if form.is_valid():
            car = form.save(commit=False)

            if car.is_featured:
                if user_can_feature_car(request.user, car):
                    if not car.featured_until or car.featured_until < timezone.now():
                        featured_days = get_featured_days(request.user)
                        car.featured_until = timezone.now() + timedelta(days=featured_days)
                else:
                    car.is_featured = False
                    car.featured_until = None
                    messages.error(
                        request,
                        'Featured ad limit reached for your package. This car was saved as a normal listing.'
                    )
            else:
                car.featured_until = None

            if request.user.is_staff or user_is_dealer(request.user):
                car.is_approved = True
            else:
                car.is_approved = False

            car.save()

            delete_image_ids = request.POST.getlist('delete_images')

            if delete_image_ids:
                car.images.filter(id__in=delete_image_ids).delete()

            primary_image_id = request.POST.get('primary_image')

            if primary_image_id and car.images.filter(id=primary_image_id).exists():
                car.images.update(is_primary=False)
                car.images.filter(id=primary_image_id).update(is_primary=True)

            images = request.FILES.getlist('images')
            current_image_count = car.images.count()

            for index, image in enumerate(images):
                car.images.create(
                    image=image,
                    is_primary=(current_image_count == 0 and index == 0),
                    sort_order=current_image_count + index
                )

            if not car.images.filter(is_primary=True).exists():
                first_image = car.images.first()
                if first_image:
                    first_image.is_primary = True
                    first_image.save()

            messages.success(request, 'Car listing updated successfully.')

            return redirect('car_detail', slug=car.slug)

    else:
        form = CarForm(instance=car)

    return render(
        request,
        'vehicles/car_form.html',
        {
            'form': form,
            'car': car,
        }
    )


@login_required
def delete_car(request, pk):
    car = get_object_or_404(
        Car,
        pk=pk,
        seller=request.user
    )

    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Car listing deleted successfully.')
        return redirect('my_listings')

    return render(
        request,
        'vehicles/delete_car.html',
        {
            'car': car
        }
    )