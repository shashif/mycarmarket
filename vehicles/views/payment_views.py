# ==========================================
# MyCarMarket
# Version: v1.1.4
# File: vehicles/views/payment_views.py
# Stripe Webhooks + Production Safe Dealer Activation
# ==========================================

import json
import stripe

from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from vehicles.models import DealerProfile, DealerSubscription, PaymentTransaction


PACKAGE_PRICE_MAP = {
    'starter': settings.STRIPE_PRICE_STARTER,
    'professional': settings.STRIPE_PRICE_PROFESSIONAL,
    'premium': settings.STRIPE_PRICE_PREMIUM,
    'enterprise': settings.STRIPE_PRICE_ENTERPRISE,
}


PACKAGE_AMOUNT_MAP = {
    'starter': Decimal('99.00'),
    'professional': Decimal('299.00'),
    'premium': Decimal('599.00'),
    'enterprise': Decimal('999.00'),
}


PACKAGE_LIMITS = {
    'starter': {
        'max_listings': 25,
        'featured_ads_allowed': 2,
        'is_featured_dealer': False,
        'priority_support': False,
    },
    'professional': {
        'max_listings': 100,
        'featured_ads_allowed': 10,
        'is_featured_dealer': False,
        'priority_support': True,
    },
    'premium': {
        'max_listings': 300,
        'featured_ads_allowed': 30,
        'is_featured_dealer': True,
        'priority_support': True,
    },
    'enterprise': {
        'max_listings': 9999,
        'featured_ads_allowed': 999,
        'is_featured_dealer': True,
        'priority_support': True,
    },
}


def activate_dealer_package(user, package_name, stripe_session):
    expiry_date = timezone.now() + timezone.timedelta(days=30)
    limits = PACKAGE_LIMITS[package_name]

    dealer_profile, created = DealerProfile.objects.get_or_create(user=user)

    dealer_profile.package = package_name
    dealer_profile.is_dealer = True
    dealer_profile.package_active = True
    dealer_profile.package_expiry = expiry_date
    dealer_profile.is_featured_dealer = limits['is_featured_dealer']
    dealer_profile.max_listings = limits['max_listings']
    dealer_profile.featured_ads_allowed = limits['featured_ads_allowed']
    dealer_profile.priority_support = limits['priority_support']
    dealer_profile.save()

    DealerSubscription.objects.update_or_create(
        user=user,
        defaults={
            'package_name': package_name,
            'monthly_price': PACKAGE_AMOUNT_MAP[package_name],
            'expires_at': expiry_date,
            'status': 'active',
            'stripe_customer_id': stripe_session.get('customer') or '',
            'stripe_subscription_id': stripe_session.get('subscription') or '',
        }
    )

    PaymentTransaction.objects.update_or_create(
        transaction_id=stripe_session.id,
        defaults={
            'user': user,
            'amount': PACKAGE_AMOUNT_MAP[package_name],
            'package_name': package_name,
            'payment_status': 'paid',
        }
    )


def deactivate_dealer_package_by_subscription(stripe_subscription_id):
    subscription = DealerSubscription.objects.filter(
        stripe_subscription_id=stripe_subscription_id
    ).first()

    if not subscription:
        return

    subscription.status = 'cancelled'
    subscription.save()

    if hasattr(subscription.user, 'dealer_profile'):
        dealer_profile = subscription.user.dealer_profile
        dealer_profile.package = 'free'
        dealer_profile.package_active = False
        dealer_profile.is_featured_dealer = False
        dealer_profile.max_listings = 3
        dealer_profile.featured_ads_allowed = 0
        dealer_profile.priority_support = False
        dealer_profile.save()


@login_required
def create_checkout_session(request, package_name):

    if package_name not in PACKAGE_PRICE_MAP:
        messages.error(request, 'Invalid dealer package selected.')
        return redirect('dealer_packages')

    price_id = PACKAGE_PRICE_MAP.get(package_name)

    if not settings.STRIPE_SECRET_KEY or not price_id:
        messages.error(request, 'Stripe payment is not configured yet.')
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
            },
            subscription_data={
                'metadata': {
                    'user_id': request.user.id,
                    'package_name': package_name,
                }
            }
        )

        PaymentTransaction.objects.update_or_create(
            transaction_id=checkout_session.id,
            defaults={
                'user': request.user,
                'amount': PACKAGE_AMOUNT_MAP[package_name],
                'package_name': package_name,
                'payment_status': 'pending',
            }
        )

        return redirect(checkout_session.url)

    except Exception as error:
        messages.error(request, f'Payment session could not be created: {error}')
        return redirect('dealer_packages')


@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        messages.error(request, 'Payment session was missing.')
        return redirect('dealer_packages')

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)

        if checkout_session.payment_status == 'paid':
            metadata_user_id = checkout_session.metadata.get('user_id')
            package_name = checkout_session.metadata.get('package_name')

            if metadata_user_id and package_name and int(metadata_user_id) == request.user.id:
                activate_dealer_package(
                    user=request.user,
                    package_name=package_name,
                    stripe_session=checkout_session
                )

        return render(
            request,
            'vehicles/payments/payment_success.html'
        )

    except Exception as error:
        messages.error(request, f'Payment verification failed: {error}')
        return redirect('dealer_packages')


@login_required
def payment_cancelled(request):
    return render(
        request,
        'vehicles/payments/payment_cancelled.html'
    )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    signature_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature_header,
            settings.STRIPE_WEBHOOK_SECRET
        )

    except ValueError:
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    event_type = event.get('type')
    data_object = event['data']['object']

    if event_type == 'checkout.session.completed':
        session = data_object

        if session.get('payment_status') == 'paid':
            metadata = session.get('metadata', {})
            user_id = metadata.get('user_id')
            package_name = metadata.get('package_name')

            if user_id and package_name in PACKAGE_LIMITS:
                try:
                    user = User.objects.get(id=user_id)
                    activate_dealer_package(
                        user=user,
                        package_name=package_name,
                        stripe_session=session
                    )
                except User.DoesNotExist:
                    pass

    if event_type == 'customer.subscription.deleted':
        stripe_subscription_id = data_object.get('id')
        deactivate_dealer_package_by_subscription(stripe_subscription_id)

    if event_type == 'invoice.payment_failed':
        stripe_subscription_id = data_object.get('subscription')

        subscription = DealerSubscription.objects.filter(
            stripe_subscription_id=stripe_subscription_id
        ).first()

        if subscription:
            subscription.status = 'cancelled'
            subscription.save()

            if hasattr(subscription.user, 'dealer_profile'):
                dealer_profile = subscription.user.dealer_profile
                dealer_profile.package_active = False
                dealer_profile.save()

    if event_type == 'invoice.paid':
        stripe_subscription_id = data_object.get('subscription')

        subscription = DealerSubscription.objects.filter(
            stripe_subscription_id=stripe_subscription_id
        ).first()

        if subscription:
            expiry_date = timezone.now() + timezone.timedelta(days=30)

            subscription.status = 'active'
            subscription.expires_at = expiry_date
            subscription.save()

            if hasattr(subscription.user, 'dealer_profile'):
                dealer_profile = subscription.user.dealer_profile
                dealer_profile.package_active = True
                dealer_profile.package_expiry = expiry_date
                dealer_profile.save()

    return HttpResponse(status=200)