# ==========================================
# MyCarMarket
# Version: v0.7.1
# File: vehicles/views/car_manage_views.py
# Create, My Listings, Edit, Delete Views
# Normal User Approval + Dealer Auto Approval
# ==========================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from vehicles.models import Car
from vehicles.forms import CarForm


def user_is_dealer(user):
    return (
        hasattr(user, 'profile') and
        user.profile.account_type == 'dealer'
    )


@login_required
def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)

        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user

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

            if car.is_approved:
                messages.success(request, 'Car listing created successfully and published.')
            else:
                messages.success(
                    request,
                    'Car listing submitted successfully. It is waiting for admin approval.'
                )

            return redirect('car_detail', pk=car.pk)

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
    cars = Car.objects.filter(
        seller=request.user
    ).order_by('-created_at')

    total_listings = cars.count()
    total_views = sum(car.views_count for car in cars)
    total_enquiries = sum(car.enquiries.count() for car in cars)

    approved_listings = cars.filter(is_approved=True).count()
    pending_listings = cars.filter(is_approved=False).count()

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

            if request.user.is_staff or user_is_dealer(request.user):
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
                messages.success(request, 'Car listing updated successfully and published.')
            else:
                messages.success(
                    request,
                    'Car listing updated successfully. It is waiting for admin approval again.'
                )

            return redirect('car_detail', pk=car.pk)

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