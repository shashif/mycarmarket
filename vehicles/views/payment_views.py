# ==========================================
# MyCarMarket
# Version: v1.1.0
# File: vehicles/views/payment_views.py
# Stripe Checkout Setup
# ==========================================

import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


PACKAGE_PRICE_MAP = {
    'starter': settings.STRIPE_PRICE_STARTER,
    'professional': settings.STRIPE_PRICE_PROFESSIONAL,
    'premium': settings.STRIPE_PRICE_PREMIUM,
    'enterprise': settings.STRIPE_PRICE_ENTERPRISE,
}


@login_required
def create_checkout_session(request, package_name):

    if package_name not in PACKAGE_PRICE_MAP:
        messages.error(request, 'Invalid dealer package selected.')
        return redirect('dealer_packages')

    price_id = PACKAGE_PRICE_MAP.get(package_name)

    if not settings.STRIPE_SECRET_KEY or not price_id:
        messages.error(
            request,
            'Stripe payment is not configured yet. Please contact admin.'
        )
        return redirect('dealer_packages')

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        checkout_session = stripe.checkout.Session.create(
            mode='subscription',
            payment_method_types=['card'],
            customer_email=request.user.email,
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                }
            ],
            success_url=(
                settings.SITE_URL
                + '/vehicles/payment-success/?session_id={CHECKOUT_SESSION_ID}'
            ),
            cancel_url=(
                settings.SITE_URL
                + '/vehicles/payment-cancelled/'
            ),
            metadata={
                'user_id': request.user.id,
                'package_name': package_name,
            }
        )

        return redirect(checkout_session.url)

    except Exception as error:
        messages.error(
            request,
            f'Payment session could not be created: {error}'
        )
        return redirect('dealer_packages')


@login_required
def payment_success(request):
    return render(
        request,
        'vehicles/payments/payment_success.html'
    )


@login_required
def payment_cancelled(request):
    return render(
        request,
        'vehicles/payments/payment_cancelled.html'
    )