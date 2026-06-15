# ==========================================
# MyCarMarket
# Version: v1.0.6
# File: vehicles/views/car_list_views.py
# Featured Cars First + Verified Cars Priority + Favourite Button Support
# ==========================================

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from vehicles.models import Car, FavouriteCar


def car_list(request):
    cars = Car.objects.filter(
        is_approved=True,
        is_active=True
    )

    query = request.GET.get('q', '').strip()

    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    min_year = request.GET.get('min_year', '').strip()
    max_year = request.GET.get('max_year', '').strip()

    suburb = request.GET.get('suburb', '').strip()
    state = request.GET.get('state', '').strip()

    transmission = request.GET.get('transmission', '').strip()
    fuel_type = request.GET.get('fuel_type', '').strip()
    body_type = request.GET.get('body_type', '').strip()

    sort_by = request.GET.get('sort_by', 'newest').strip()

    if query:
        cars = cars.filter(
            Q(title__icontains=query) |
            Q(make__icontains=query) |
            Q(model__icontains=query) |
            Q(suburb__icontains=query) |
            Q(state__icontains=query) |
            Q(description__icontains=query)
        )

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)

    if min_year:
        cars = cars.filter(year__gte=min_year)

    if max_year:
        cars = cars.filter(year__lte=max_year)

    if suburb:
        cars = cars.filter(suburb__icontains=suburb)

    if state:
        cars = cars.filter(state=state)

    if transmission:
        cars = cars.filter(transmission=transmission)

    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)

    if body_type:
        cars = cars.filter(body_type=body_type)

    if sort_by == 'oldest':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            'created_at'
        )

    elif sort_by == 'price_low':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            'price'
        )

    elif sort_by == 'price_high':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            '-price'
        )

    elif sort_by == 'km_low':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            'kilometres'
        )

    elif sort_by == 'km_high':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            '-kilometres'
        )

    elif sort_by == 'year_new':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            '-year'
        )

    elif sort_by == 'year_old':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            'year'
        )

    else:
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            '-created_at'
        )

    favourite_car_ids = []

    if request.user.is_authenticated:
        favourite_car_ids = list(
            FavouriteCar.objects.filter(
                user=request.user
            ).values_list('car_id', flat=True)
        )

    paginator = Paginator(cars, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'vehicles/car_list.html',
        {
            'cars': page_obj,
            'page_obj': page_obj,
            'query': query,
            'min_price': min_price,
            'max_price': max_price,
            'min_year': min_year,
            'max_year': max_year,
            'suburb': suburb,
            'state': state,
            'transmission': transmission,
            'fuel_type': fuel_type,
            'body_type': body_type,
            'sort_by': sort_by,
            'favourite_car_ids': favourite_car_ids,
        }
    )


# ==========================================
# END CAR LIST VIEW
# ==========================================