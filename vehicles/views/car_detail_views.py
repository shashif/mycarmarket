# ==========================================
# MyCarMarket
# Version: v1.4.3
# File: vehicles/views/car_detail_views.py
# Car Detail + Finance Calculator + Enquiry + Favourite + Recently Viewed
# ==========================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from core.models import SiteSettings

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

    # ==========================================
    # FINANCE CALCULATOR
    # ==========================================

    car_price = float(car.price)

    deposit = request.GET.get('deposit', '')
    interest_rate = request.GET.get('interest_rate', '')
    loan_years = request.GET.get('loan_years', '')

    try:
        deposit_value = float(deposit) if deposit else 0
    except ValueError:
        deposit_value = 0

    try:
        interest_rate_value = float(interest_rate) if interest_rate else 8.99
    except ValueError:
        interest_rate_value = 8.99

    try:
        loan_years_value = int(loan_years) if loan_years else 5
    except ValueError:
        loan_years_value = 5

    if deposit_value < 0:
        deposit_value = 0

    if deposit_value > car_price:
        deposit_value = car_price

    if interest_rate_value < 0:
        interest_rate_value = 0

    if loan_years_value < 1:
        loan_years_value = 1

    loan_amount = car_price - deposit_value
    total_months = loan_years_value * 12
    monthly_rate = interest_rate_value / 100 / 12

    if loan_amount > 0 and monthly_rate > 0:
        monthly_payment = (
            loan_amount
            * monthly_rate
            * ((1 + monthly_rate) ** total_months)
        ) / (((1 + monthly_rate) ** total_months) - 1)
    else:
        monthly_payment = loan_amount / total_months if total_months > 0 else 0

    total_repayment = monthly_payment * total_months
    total_interest = total_repayment - loan_amount

    finance_data = {
        'deposit': round(deposit_value, 2),
        'interest_rate': interest_rate_value,
        'loan_years': loan_years_value,
        'loan_amount': round(loan_amount, 2),
        'monthly_payment': round(monthly_payment, 2),
        'total_repayment': round(total_repayment, 2),
        'total_interest': round(total_interest, 2),
    }

    # ==========================================
    # RECENTLY VIEWED
    # ==========================================

    recently_viewed = request.session.get('recently_viewed_cars', [])

    if car.id in recently_viewed:
        recently_viewed.remove(car.id)

    recently_viewed.insert(0, car.id)

    request.session['recently_viewed_cars'] = recently_viewed[:6]
    request.session.modified = True

    recent_ids = request.session.get('recently_viewed_cars', [])

    recently_viewed_cars = []

    for recent_id in recent_ids:
        if recent_id != car.id:
            recent_car = Car.objects.filter(
                id=recent_id,
                is_approved=True,
                is_active=True
            ).first()

            if recent_car:
                recently_viewed_cars.append(recent_car)

    images = car.images.all()

    share_url = request.build_absolute_uri()

    share_text = (
        f"Check out this {car.year} {car.make} {car.model} "
        f"on MyCarMarket Australia"
    )

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

        if (today.month, today.day) < (
            dealer_member_since.month,
            dealer_member_since.day
        ):
            dealer_years_active -= 1

    similar_cars = Car.objects.filter(
        is_approved=True,
        is_active=True,
        make__iexact=car.make,
        body_type=car.body_type
    ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True,
            is_active=True,
            make__iexact=car.make
        ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True,
            is_active=True,
            body_type=car.body_type
        ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True,
            is_active=True
        ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if request.method == 'POST':

        form = EnquiryForm(request.POST)

        if form.is_valid():

            enquiry = form.save(commit=False)
            enquiry.car = car
            enquiry.dealer = car.seller
            enquiry.save()

            seller_email = ''

            if car.seller and car.seller.email:
                seller_email = car.seller.email

            elif car.seller_email:
                seller_email = car.seller_email

            if seller_email:

                subject = f"New enquiry for {car.title} - MyCarMarket Australia"

                message = (
                    f"Hello,\n\n"
                    f"You have received a new enquiry on MyCarMarket Australia.\n\n"
                    f"Car Details:\n"
                    f"{car.year} {car.make} {car.model}\n"
                    f"Title: {car.title}\n"
                    f"Price: ${car.price}\n"
                    f"Kilometres: {car.kilometres} km\n"
                    f"Location: {car.display_location()}\n\n"
                    f"Buyer Details:\n"
                    f"Name: {enquiry.name}\n"
                    f"Email: {enquiry.email}\n"
                    f"Phone: {enquiry.phone}\n\n"
                    f"Message:\n"
                    f"{enquiry.message}\n\n"
                    f"Listing Link:\n"
                    f"{share_url}\n\n"
                    f"Regards,\n"
                    f"MyCarMarket Australia"
                )

                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [seller_email],
                        fail_silently=True
                    )
                except Exception:
                    pass

            messages.success(
                request,
                'Your enquiry has been sent successfully.'
            )

            return redirect('car_detail', slug=car.slug)

    else:

        initial_message = (
            f"Hi, I am interested in this car:\n\n"
            f"{car.year} {car.make} {car.model}\n"
            f"Price: ${car.price}\n"
            f"Estimated finance from ${finance_data['monthly_payment']} per month\n"
            f"Kilometres: {car.kilometres} km\n"
            f"Location: {car.display_location()}\n\n"
            f"Please contact me with more information."
        )

        form = EnquiryForm(
            initial={
                'message': initial_message
            }
        )

    settings_obj = SiteSettings.objects.first()

    return render(
        request,
        'vehicles/car_detail.html',
        {
            'car': car,
            'images': images,
            'similar_cars': similar_cars,
            'recently_viewed_cars': recently_viewed_cars,
            'form': form,
            'share_url': share_url,
            'share_text': share_text,
            'is_favourite': is_favourite,
            'dealer_active_cars_count': dealer_active_cars_count,
            'dealer_featured_cars_count': dealer_featured_cars_count,
            'dealer_member_since': dealer_member_since,
            'dealer_years_active': dealer_years_active,
            'settings': settings_obj,
            'finance_data': finance_data,
        }
    )