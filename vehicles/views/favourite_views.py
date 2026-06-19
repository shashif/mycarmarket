# ==========================================
# MyCarMarket
# Version: v1.3.0
# File: vehicles/views/favourite_views.py
# Favourite Cars Save / Unsave / List + AJAX Support
# ==========================================

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

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
        is_favourited = True
        message = 'Car saved to your favourites.'
    else:
        favourite.delete()
        is_favourited = False
        message = 'Car removed from your favourites.'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_favourited': is_favourited,
            'message': message
        })

    messages.success(request, message)

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