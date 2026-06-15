# ==========================================
# MyCarMarket
# Version: v1.0.6
# File: vehicles/views/favourite_views.py
# Favourite Cars Save / Unsave / List + Smart Redirect
# ==========================================

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from vehicles.models import Car, FavouriteCar


@login_required
def toggle_favourite(request, slug):
    car = get_object_or_404(
        Car,
        slug=slug,
        is_approved=True,
        is_active=True
    )

    favourite, created = FavouriteCar.objects.get_or_create(
        user=request.user,
        car=car
    )

    if created:
        messages.success(request, 'Car saved to your favourites.')
    else:
        favourite.delete()
        messages.success(request, 'Car removed from your favourites.')

    next_url = request.POST.get('next') or request.GET.get('next')

    if next_url:
        return redirect(next_url)

    return redirect(
        'car_detail',
        slug=car.slug
    )


@login_required
def saved_cars(request):
    favourites = FavouriteCar.objects.filter(
        user=request.user,
        car__is_approved=True,
        car__is_active=True
    ).select_related('car').order_by('-created_at')

    return render(
        request,
        'vehicles/saved_cars.html',
        {
            'favourites': favourites
        }
    )


# ==========================================
# END FAVOURITE VIEWS
# ==========================================