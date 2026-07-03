# ==========================================
# MyCarMarket
# Version: v1.5.3
# File: vehicles/views/car_detail_views.py
# Description: Car Detail + Finance Calculator + Enquiry Email + Moderation Protection
# ==========================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg

from core.models import SiteSettings

from vehicles.models import Car, FavouriteCar
from vehicles.forms import EnquiryForm


# ==========================================
# SECTION 01: CAR DETAIL VIEW
# START
# ==========================================

def car_detail(request, slug):

    car = get_object_or_404(Car, slug=slug)

    # ==========================================
    # SECTION 02: MODERATION PROTECTION
    # START
    # ==========================================

    if car.moderation_status != 'approved':

        if not request.user.is_authenticated:
            messages.error(
                request,
                'This listing is currently unavailable.'
            )
            return redirect('car_list')

        if (
            car.seller != request.user
            and not request.user.is_staff
        ):
            messages.error(
                request,
                'This listing is currently unavailable.'
            )
            return redirect('car_list')

    # ==========================================
    # SECTION 02: MODERATION PROTECTION
    # END
    # ==========================================

    # ==========================================
    # SECTION 03: VIEW COUNT
    # START
    # ==========================================

    car.views_count += 1
    car.save(update_fields=['views_count'])

    # ==========================================
    # SECTION 03: VIEW COUNT
    # END
    # ==========================================

    # ==========================================
    # SECTION 04: FINANCE CALCULATOR
    # START
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
    # SECTION 04: FINANCE CALCULATOR
    # END
    # ==========================================

    # ==========================================
    # SECTION 05: AI PRICE INSIGHT
    # START
    # ==========================================

    minimum_comparable_count = 5

    ai_comparable_cars = Car.objects.filter(
        is_approved=True,
        is_active=True,
        moderation_status='approved',
        make__iexact=car.make,
        model__iexact=car.model,
        year__gte=car.year - 2,
        year__lte=car.year + 2
    ).exclude(pk=car.pk)

    ai_comparison_type = 'similar make, model and year'

    if ai_comparable_cars.count() < minimum_comparable_count:
        ai_comparable_cars = Car.objects.filter(
            is_approved=True,
            is_active=True,
            moderation_status='approved',
            make__iexact=car.make,
            model__iexact=car.model
        ).exclude(pk=car.pk)

        ai_comparison_type = 'similar make and model'

    if ai_comparable_cars.count() < minimum_comparable_count:
        ai_comparable_cars = Car.objects.filter(
            is_approved=True,
            is_active=True,
            moderation_status='approved',
            make__iexact=car.make,
            body_type=car.body_type
        ).exclude(pk=car.pk)

        ai_comparison_type = 'similar make and body type'

    comparable_count = ai_comparable_cars.count()

    ai_price_insight = {
        'has_data': False,
        'label': 'Not Enough Data',
        'status': 'neutral',
        'average_market_price': None,
        'current_price': round(car_price, 2),
        'price_difference': None,
        'comparison_count': comparable_count,
        'comparison_type': ai_comparison_type,
        'message': (
            'There are not enough similar vehicles listed on '
            'MyCarMarket Australia to provide a reliable price insight yet.'
        ),
    }

    if comparable_count >= minimum_comparable_count:

        average_market_price = ai_comparable_cars.aggregate(
            average_price=Avg('price')
        )['average_price']

        if average_market_price:
            average_market_price_value = float(average_market_price)
            price_difference = car_price - average_market_price_value

            difference_percent = (
                price_difference / average_market_price_value
            ) * 100 if average_market_price_value > 0 else 0

            if difference_percent <= -8:
                label = 'Great Value'
                status = 'great'
                message = (
                    'This vehicle appears to be priced below similar vehicles '
                    'currently listed on MyCarMarket Australia.'
                )

            elif difference_percent >= 8:
                label = 'Above Market'
                status = 'above'
                message = (
                    'This vehicle appears to be priced above similar vehicles '
                    'currently listed on MyCarMarket Australia.'
                )

            else:
                label = 'Fair Price'
                status = 'fair'
                message = (
                    'This vehicle appears to be priced within the typical range '
                    'for similar vehicles currently listed on MyCarMarket Australia.'
                )

            ai_price_insight = {
                'has_data': True,
                'label': label,
                'status': status,
                'average_market_price': round(average_market_price_value, 2),
                'current_price': round(car_price, 2),
                'price_difference': round(price_difference, 2),
                'comparison_count': comparable_count,
                'comparison_type': ai_comparison_type,
                'message': message,
            }

    # ==========================================
    # SECTION 05: AI PRICE INSIGHT
    # END
    # ==========================================

    # ==========================================
    # SECTION 06: RECENTLY VIEWED CARS
    # START
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
                is_active=True,
                moderation_status='approved'
            ).first()

            if recent_car:
                recently_viewed_cars.append(recent_car)

    # ==========================================
    # SECTION 06: RECENTLY VIEWED CARS
    # END
    # ==========================================

    # ==========================================
    # SECTION 07: SHARE + FAVOURITE
    # START
    # ==========================================

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

    # ==========================================
    # SECTION 07: SHARE + FAVOURITE
    # END
    # ==========================================

    # ==========================================
    # SECTION 08: DEALER STATS
    # START
    # ==========================================

    dealer_active_cars_count = 0
    dealer_featured_cars_count = 0
    dealer_member_since = None
    dealer_years_active = 0

    if car.seller:

        dealer_active_cars_count = Car.objects.filter(
            seller=car.seller,
            is_approved=True,
            is_active=True,
            moderation_status='approved'
        ).count()

        dealer_featured_cars_count = Car.objects.filter(
            seller=car.seller,
            is_approved=True,
            is_active=True,
            moderation_status='approved',
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

    # ==========================================
    # SECTION 08: DEALER STATS
    # END
    # ==========================================

    # ==========================================
    # SECTION 09: SIMILAR CARS
    # START
    # ==========================================

    similar_cars = Car.objects.filter(
        is_approved=True,
        is_active=True,
        moderation_status='approved',
        make__iexact=car.make,
        body_type=car.body_type
    ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True,
            is_active=True,
            moderation_status='approved',
            make__iexact=car.make
        ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True,
            is_active=True,
            moderation_status='approved',
            body_type=car.body_type
        ).exclude(pk=car.pk).order_by('-created_at')[:6]

    if not similar_cars.exists():
        similar_cars = Car.objects.filter(
            is_approved=True,
            is_active=True,
            moderation_status='approved'
        ).exclude(pk=car.pk).order_by('-created_at')[:6]

    # ==========================================
    # SECTION 09: SIMILAR CARS
    # END
    # ==========================================

       # ==========================================
    # SECTION 10: ENQUIRY FORM + EMAIL
    # START
    # ==========================================

    if request.method == 'POST':

        form = EnquiryForm(request.POST)

        if form.is_valid():

            enquiry = form.save(commit=False)
            enquiry.car = car
            enquiry.dealer = car.seller
            enquiry.save()

            enquiry_reference = f"ENQ-{enquiry.id:06d}"

            # ==========================================
            # SECTION 10.1: SELLER EMAIL DETECTION
            # START
            # ==========================================

            seller_email = ''

            if car.seller_email:
                seller_email = car.seller_email.strip()

            elif car.seller and car.seller.email:
                seller_email = car.seller.email.strip()

            # ==========================================
            # SECTION 10.1: SELLER EMAIL DETECTION
            # END
            # ==========================================

            seller_subject = (
                f"{enquiry_reference} - New enquiry for {car.title}"
            )

            seller_message = (
                f"Hello,\n\n"
                f"You have received a new enquiry on MyCarMarket Australia.\n\n"
                f"Enquiry Reference: {enquiry_reference}\n\n"
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

            buyer_subject = (
                f"{enquiry_reference} - Your enquiry was sent"
            )

            buyer_message = (
                f"Hello {enquiry.name},\n\n"
                f"Thank you for using MyCarMarket Australia.\n\n"
                f"Your enquiry has been sent to the seller.\n\n"
                f"Enquiry Reference: {enquiry_reference}\n\n"
                f"Car Details:\n"
                f"{car.year} {car.make} {car.model}\n"
                f"Title: {car.title}\n"
                f"Price: ${car.price}\n"
                f"Kilometres: {car.kilometres} km\n"
                f"Location: {car.display_location()}\n\n"
                f"Your Message:\n"
                f"{enquiry.message}\n\n"
                f"Listing Link:\n"
                f"{share_url}\n\n"
                f"Regards,\n"
                f"MyCarMarket Australia"
            )

            admin_subject = (
                f"{enquiry_reference} - New enquiry received"
            )

            admin_message = (
                f"New enquiry received on MyCarMarket Australia.\n\n"
                f"Enquiry Reference: {enquiry_reference}\n\n"
                f"Car: {car.year} {car.make} {car.model}\n"
                f"Title: {car.title}\n"
                f"Price: ${car.price}\n"
                f"Location: {car.display_location()}\n\n"
                f"Buyer:\n"
                f"Name: {enquiry.name}\n"
                f"Email: {enquiry.email}\n"
                f"Phone: {enquiry.phone}\n\n"
                f"Seller Email: {seller_email or 'No seller email'}\n\n"
                f"Message:\n"
                f"{enquiry.message}\n\n"
                f"Listing Link:\n"
                f"{share_url}"
            )

            try:
                if seller_email:
                    send_mail(
                        seller_subject,
                        seller_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [seller_email],
                        fail_silently=False
                    )

                if enquiry.email:
                    send_mail(
                        buyer_subject,
                        buyer_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [enquiry.email],
                        fail_silently=False
                    )

                admin_email = getattr(
                    settings,
                    'CONTACT_EMAIL',
                    ''
                )

                if admin_email:
                    send_mail(
                        admin_subject,
                        admin_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [admin_email],
                        fail_silently=False
                    )

            except Exception as e:
                messages.warning(
                    request,
                    f'Your enquiry was saved, but email notification could not be sent. Error: {e}'
                )

                return redirect('car_detail', slug=car.slug)

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

    # ==========================================
    # SECTION 10: ENQUIRY FORM + EMAIL
    # END
    # ==========================================

    # ==========================================
    # SECTION 11: SITE SETTINGS + RENDER
    # START
    # ==========================================

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
            'ai_price_insight': ai_price_insight,
        }
    )

# ==========================================
# SECTION 11: SITE SETTINGS + RENDER
# END
# ==========================================


# ==========================================
# SECTION 01: CAR DETAIL VIEW
# END
# ==========================================


# ==========================================
# END FILE
# ==========================================