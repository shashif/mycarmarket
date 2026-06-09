# ==========================================
# MyCarMarket
# Version: v0.8.3
# File: vehicles/views/car_detail_views.py
# Dealer Trust + Enquiry + Favourite Status
# ==========================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from vehicles.models import Car, FavouriteCar
from vehicles.forms import EnquiryForm


def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)

    if not car.is_approved:
        if not request.user.is_authenticated:
            messages.error(request, 'This listing is waiting for admin approval.')
            return redirect('car_list')

        if car.seller != request.user and not request.user.is_staff:
            messages.error(request, 'This listing is waiting for admin approval.')
            return redirect('car_list')

    car.views_count += 1
    car.save(update_fields=['views_count'])

    images = car.images.all()

    share_url = request.build_absolute_uri()
    share_text = f"Check out this {car.year} {car.make} {car.model} on MyCarMarket Australia"

    is_favourite = False

    if request.user.is_authenticated:
        is_favourite = FavouriteCar.objects.filter(
            user=request.user,
            car=car
        ).exists()

    dealer_active_cars_count = 0
    dealer_featured_cars_count = 0
    dealer_member_since = None
    dealer_years_active = 0

    if car.seller:
        dealer_active_cars_count = Car.objects.filter(
            seller=car.seller,
            is_approved=True,
            is_active=True
        ).count()

        dealer_featured_cars_count = Car.objects.filter(
            seller=car.seller,
            is_approved=True,
            is_active=True,
            is_featured=True
        ).count()

        dealer_member_since = car.seller.date_joined

        today = timezone.now()
        dealer_years_active = today.year - dealer_member_since.year

        if (
            today.month,
            today.day
        ) < (
            dealer_member_since.month,
            dealer_member_since.day
        ):
            dealer_years_active -= 1

    similar_cars = Car.objects.filter(
        is_approved=True,
        make__iexact=car.make,
        body_type=car.body_type
    ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True,
            make__iexact=car.make
        ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True,
            body_type=car.body_type
        ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True
        ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if request.method == 'POST':
        form = EnquiryForm(request.POST)

        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.car = car
            enquiry.save()

            messages.success(request, 'Your enquiry has been sent successfully.')
            return redirect('car_detail', slug=car.slug)

    else:
        initial_message = (
            f"Hi, I am interested in this car:\n\n"
            f"{car.year} {car.make} {car.model}\n"
            f"Price: ${car.price}\n"
            f"Kilometres: {car.kilometres} km\n"
            f"Location: {car.display_location()}\n\n"
            f"Please contact me with more information."
        )

        form = EnquiryForm(
            initial={
                'message': initial_message
            }
        )

    return render(
        request,
        'vehicles/car_detail.html',
        {
            'car': car,
            'images': images,
            'similar_cars': similar_cars,
            'form': form,
            'share_url': share_url,
            'share_text': share_text,
            'is_favourite': is_favourite,
            'dealer_active_cars_count': dealer_active_cars_count,
            'dealer_featured_cars_count': dealer_featured_cars_count,
            'dealer_member_since': dealer_member_since,
            'dealer_years_active': dealer_years_active,
        }
    )