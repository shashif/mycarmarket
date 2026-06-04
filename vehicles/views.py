# ==========================================
# MyCarMarket
# Version: v0.3.6 - View Counter + Listed Date + Trust Badges
# File: vehicles/views.py
# ==========================================

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.contrib import messages

from .models import Car
from .forms import EnquiryForm


def car_list(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_year = request.GET.get('min_year', '')
    max_year = request.GET.get('max_year', '')
    location = request.GET.get('location', '')
    transmission = request.GET.get('transmission', '')
    fuel_type = request.GET.get('fuel_type', '')
    body_type = request.GET.get('body_type', '')
    sort_by = request.GET.get('sort_by', 'newest')

    cars = Car.objects.prefetch_related('images').filter(is_active=True)

    if query:
        cars = cars.filter(
            Q(title__icontains=query) |
            Q(make__icontains=query) |
            Q(model__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(transmission__icontains=query) |
            Q(fuel_type__icontains=query) |
            Q(body_type__icontains=query)
        )

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)

    if min_year:
        cars = cars.filter(year__gte=min_year)

    if max_year:
        cars = cars.filter(year__lte=max_year)

    if location:
        cars = cars.filter(location__icontains=location)

    if transmission:
        cars = cars.filter(transmission__icontains=transmission)

    if fuel_type:
        cars = cars.filter(fuel_type__icontains=fuel_type)

    if body_type:
        cars = cars.filter(body_type__icontains=body_type)

    if sort_by == 'oldest':
        cars = cars.order_by('created_at')
    elif sort_by == 'price_low':
        cars = cars.order_by('price')
    elif sort_by == 'price_high':
        cars = cars.order_by('-price')
    elif sort_by == 'km_low':
        cars = cars.order_by('kilometres')
    elif sort_by == 'km_high':
        cars = cars.order_by('-kilometres')
    elif sort_by == 'year_new':
        cars = cars.order_by('-year')
    elif sort_by == 'year_old':
        cars = cars.order_by('year')
    else:
        cars = cars.order_by('-created_at')

    paginator = Paginator(cars, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'vehicles/car_list.html',
        {
            'page_obj': page_obj,
            'query': query,
            'min_price': min_price,
            'max_price': max_price,
            'min_year': min_year,
            'max_year': max_year,
            'location': location,
            'transmission': transmission,
            'fuel_type': fuel_type,
            'body_type': body_type,
            'sort_by': sort_by,
        }
    )


def car_detail(request, car_id):
    car = get_object_or_404(
        Car.objects.prefetch_related('images'),
        id=car_id,
        is_active=True
    )

    if request.method == 'GET':
        Car.objects.filter(id=car.id).update(views_count=F('views_count') + 1)
        car.refresh_from_db(fields=['views_count'])

    images = car.images.all().order_by('-is_primary', 'sort_order', 'id')

    default_message = (
        f"Hi, I am interested in this car.\n\n"
        f"Car: {car.title}\n"
        f"Make: {car.make}\n"
        f"Model: {car.model}\n"
        f"Year: {car.year}\n"
        f"Kilometres: {car.kilometres} km\n"
        f"Transmission: {car.transmission or 'Not specified'}\n"
        f"Fuel Type: {car.fuel_type or 'Not specified'}\n"
        f"Body Type: {car.body_type or 'Not specified'}\n"
        f"Location: {car.location or 'Not specified'}\n"
        f"Price: ${car.price}\n\n"
        f"Is this car still available? Please contact me when possible."
    )

    similar_cars = (
        Car.objects
        .prefetch_related('images')
        .filter(is_active=True)
        .exclude(id=car.id)
        .filter(
            Q(make__iexact=car.make) |
            Q(model__iexact=car.model) |
            Q(body_type__iexact=car.body_type) |
            Q(fuel_type__iexact=car.fuel_type) |
            Q(transmission__iexact=car.transmission)
        )
        .order_by('-is_featured', '-created_at')[:4]
    )

    if not similar_cars.exists():
        similar_cars = (
            Car.objects
            .prefetch_related('images')
            .filter(is_active=True)
            .exclude(id=car.id)
            .order_by('-is_featured', '-created_at')[:4]
        )

    if request.method == 'POST':
        form = EnquiryForm(request.POST)

        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.car = car
            enquiry.save()

            messages.success(
                request,
                'Your enquiry has been sent successfully. The seller will contact you soon.'
            )

            return redirect('car_detail', car_id=car.id)

    else:
        form = EnquiryForm(
            initial={
                'message': default_message
            }
        )

    return render(
        request,
        'vehicles/car_detail.html',
        {
            'car': car,
            'images': images,
            'form': form,
            'similar_cars': similar_cars,
        }
    )