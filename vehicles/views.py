# ==========================================
# MyCarMarket
# Version: v0.6.1
# Dealer Profile Page
# ==========================================


# ==========================================
# START SECTION 1: IMPORTS
# ==========================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Car
from .forms import CarForm, EnquiryForm
from django.contrib.auth.models import User
# ==========================================
# END SECTION 1: IMPORTS
# ==========================================


# ==========================================
# START SECTION 2: CAR LIST PAGE
# ==========================================

def car_list(request):
    cars = Car.objects.filter(is_approved=True)

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
        }
    )

# ==========================================
# END SECTION 2: CAR LIST PAGE
# ==========================================


# ==========================================
# START SECTION 3: CAR DETAIL PAGE + ENQUIRY
# ==========================================

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if not car.is_approved:
        if not request.user.is_authenticated:
            messages.error(
                request,
                'This listing is waiting for admin approval.'
            )
            return redirect('car_list')

        if car.seller != request.user and not request.user.is_staff:
            messages.error(
                request,
                'This listing is waiting for admin approval.'
            )
            return redirect('car_list')

    car.views_count += 1
    car.save(update_fields=['views_count'])

    images = car.images.all()

    similar_cars = Car.objects.filter(
        is_approved=True,
        make__icontains=car.make
    ).exclude(
        pk=car.pk
    ).order_by('-created_at')[:4]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True
        ).exclude(
            pk=car.pk
        ).order_by('-created_at')[:4]

    if request.method == 'POST':

        form = EnquiryForm(request.POST)

        if form.is_valid():

            enquiry = form.save(commit=False)
            enquiry.car = car
            enquiry.save()

            messages.success(
                request,
                'Your enquiry has been sent successfully.'
            )

            return redirect(
                'car_detail',
                pk=car.pk
            )

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
        }
    )

# ==========================================
# END SECTION 3: CAR DETAIL PAGE + ENQUIRY
# ==========================================


# ==========================================
# START SECTION 4: CREATE CAR LISTING
# ==========================================

@login_required
def create_car(request):

    if request.method == 'POST':

        form = CarForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            car = form.save(commit=False)
            car.seller = request.user

            if request.user.is_staff:
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

            if car.is_approved:
                messages.success(
                    request,
                    'Car listing created successfully.'
                )
            else:
                messages.success(
                    request,
                    'Car listing submitted successfully. It is waiting for admin approval.'
                )

            return redirect(
                'car_detail',
                pk=car.pk
            )

    else:

        form = CarForm()

    return render(
        request,
        'vehicles/car_form.html',
        {
            'form': form
        }
    )

# ==========================================
# END SECTION 4: CREATE CAR LISTING
# ==========================================


# ==========================================
# START SECTION 5: MY LISTINGS / SELLER DASHBOARD
# ==========================================

@login_required
def my_listings(request):

    cars = Car.objects.filter(
        seller=request.user
    ).order_by('-created_at')

    total_listings = cars.count()

    total_views = sum(
        car.views_count for car in cars
    )

    total_enquiries = sum(
        car.enquiries.count() for car in cars
    )

    approved_listings = cars.filter(
        is_approved=True
    ).count()

    pending_listings = cars.filter(
        is_approved=False
    ).count()

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
        }
    )

# ==========================================
# END SECTION 5: MY LISTINGS / SELLER DASHBOARD
# ==========================================


# ==========================================
# START SECTION 6: EDIT CAR LISTING
# ==========================================

@login_required
def edit_car(request, pk):

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

            if request.user.is_staff:
                car.is_approved = True
            else:
                car.is_approved = False

            car.save()

            images = request.FILES.getlist('images')

            for index, image in enumerate(images):

                car.images.create(
                    image=image,
                    is_primary=False,
                    sort_order=index
                )

            if car.is_approved:
                messages.success(
                    request,
                    'Car listing updated successfully.'
                )
            else:
                messages.success(
                    request,
                    'Car listing updated successfully. It is waiting for admin approval again.'
                )

            return redirect(
                'car_detail',
                pk=car.pk
            )

    else:

        form = CarForm(
            instance=car
        )

    return render(
        request,
        'vehicles/car_form.html',
        {
            'form': form,
            'car': car,
        }
    )

# ==========================================
# END SECTION 6: EDIT CAR LISTING
# ==========================================


# ==========================================
# START SECTION 7: DELETE CAR LISTING
# ==========================================

@login_required
def delete_car(request, pk):

    car = get_object_or_404(
        Car,
        pk=pk,
        seller=request.user
    )

    if request.method == 'POST':

        car.delete()

        messages.success(
            request,
            'Car listing deleted successfully.'
        )

        return redirect(
            'my_listings'
        )

    return render(
        request,
        'vehicles/delete_car.html',
        {
            'car': car
        }
    )

# ==========================================
# END SECTION 7: DELETE CAR LISTING
# ==========================================

def dealer_detail(request, user_id):

    dealer = get_object_or_404(
        User,
        id=user_id
    )

    cars = Car.objects.filter(
        seller=dealer,
        is_approved=True
    ).order_by('-created_at')

    share_url = request.build_absolute_uri()

    return render(
        request,
        'vehicles/dealer_detail.html',
        {
            'dealer': dealer,
            'cars': cars,
            'share_url': share_url,
        }
    )