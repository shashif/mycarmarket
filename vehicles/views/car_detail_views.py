# ==========================================
# MyCarMarket
# Version: v0.7.0
# File: vehicles/views/car_detail_views.py
# SEO Slug Detail Page + Enquiry + Share Link
# ==========================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from vehicles.models import Car
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

    similar_cars = Car.objects.filter(
        is_approved=True,
        make__icontains=car.make
    ).exclude(pk=car.pk).order_by('-created_at')[:4]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True
        ).exclude(pk=car.pk).order_by('-created_at')[:4]

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
        }
    )