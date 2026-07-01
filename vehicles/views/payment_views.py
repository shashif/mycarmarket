# ==========================================
# MyCarMarket
# Version: v1.5.1
# File: vehicles/views/payment_views.py
# Description: Stripe Payments Using Admin-Controlled Site Settings
# ==========================================

import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from core.models import SiteSettings

from vehicles.models import (
    DealerProfile,
    DealerSubscription,
    PaymentTransaction,
    DealerPackage,
)


# ==========================================
# SECTION 01: SITE SETTINGS HELPERS
# ==========================================

def get_site_settings():
    return SiteSettings.objects.first()


def get_stripe_secret_key():
    site_settings = get_site_settings()

    if not site_settings:
        return ""

    return site_settings.stripe_secret_key


def get_stripe_webhook_secret():
    site_settings = get_site_settings()

    if not site_settings:
        return ""

    return site_settings.stripe_webhook_secret


# ==========================================
# SECTION 02: PACKAGE HELPERS
# ==========================================

def get_dealer_package(package_name):
    return DealerPackage.objects.filter(
        name=package_name,
        is_active=True
    ).first()


def get_stripe_price_id(site_settings, package_name):
    if not site_settings:
        return ''

    price_map = {
        'starter': site_settings.stripe_price_starter,
        'professional': site_settings.stripe_price_professional,
        'premium': site_settings.stripe_price_premium,
        'enterprise': site_settings.stripe_price_enterprise,
    }

    return price_map.get(package_name, '')


# ==========================================
# SECTION 03: EMAIL HELPERS
# ==========================================

def send_dealer_payment_email(user, package_name, expiry_date):
    if not user.email:
        return

    subject = f"Your {package_name.title()} package is active - MyCarMarket Australia"

    message = (
        f"Hello {user.username},\n\n"
        f"Your dealer package is now active.\n\n"
        f"Package: {package_name.title()}\n"
        f"Expiry Date: {expiry_date.strftime('%d %B %Y')}\n\n"
        f"Dealer Dashboard:\n"
        f"{settings.SITE_URL}/cars/dealer/dashboard/\n\n"
        f"Regards,\n"
        f"MyCarMarket Australia"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def send_admin_payment_email(user, package_name, expiry_date):
    admin_email = getattr(settings, 'CONTACT_EMAIL', '')

    if not admin_email:
        return

    subject = f"New dealer subscription - {package_name.title()}"

    message = (
        f"A dealer package has been activated.\n\n"
        f"User: {user.username}\n"
        f"Email: {user.email}\n"
        f"Package: {package_name.title()}\n"
        f"Expiry Date: {expiry_date.strftime('%d %B %Y')}\n\n"
        f"MyCarMarket Australia"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [admin_email],
        fail_silently=False,
    )


def send_payment_failed_email(user):
    if not user.email:
        return

    subject = "Payment failed - MyCarMarket Australia"

    message = (
        f"Hello {user.username},\n\n"
        f"We were unable to process your dealer subscription payment.\n\n"
        f"Please contact MyCarMarket support if you need help.\n\n"
        f"Regards,\n"
        f"MyCarMarket Australia"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


# ==========================================
# SECTION 04: DEALER ACTIVATION
# ==========================================

def activate_dealer_package(user, package_name, stripe_session):
    package = get_dealer_package(package_name)

    if not package:
        return

    expiry_date = timezone.now() + timezone.timedelta(days=30)

    dealer_profile, created = DealerProfile.objects.get_or_create(
        user=user
    )

    dealer_profile.package = package.name
    dealer_profile.is_dealer = True
    dealer_profile.package_active = True
    dealer_profile.package_expiry = expiry_date
    dealer_profile.is_featured_dealer = package.is_featured_dealer
    dealer_profile.max_listings = package.max_listings
    dealer_profile.featured_ads_allowed = package.featured_ads_allowed
    dealer_profile.priority_support = package.priority_support
    dealer_profile.save()

    DealerSubscription.objects.update_or_create(
        user=user,
        defaults={
            'package_name': package.name,
            'monthly_price': package.monthly_price,
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
            'amount': package.monthly_price,
            'package_name': package.name,
            'payment_status': 'paid',
        }
    )

    try:
        send_dealer_payment_email(
            user=user,
            package_name=package.name,
            expiry_date=expiry_date,
        )

        send_admin_payment_email(
            user=user,
            package_name=package.name,
            expiry_date=expiry_date,
        )

    except Exception:
        pass


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


# ==========================================
# SECTION 05: CREATE STRIPE CHECKOUT SESSION
# ==========================================

@login_required
def create_checkout_session(request, package_name):
    site_settings = get_site_settings()

    if not site_settings or not site_settings.stripe_enabled:
        messages.error(request, 'Stripe payment is currently disabled.')
        return redirect('dealer_packages')

    package = get_dealer_package(package_name)

    if not package:
        messages.error(request, 'Invalid or inactive dealer package selected.')
        return redirect('dealer_packages')

    price_id = get_stripe_price_id(site_settings, package_name)
    stripe_secret_key = get_stripe_secret_key()

    if not stripe_secret_key or not price_id:
        messages.error(request, 'Stripe payment is not configured yet.')
        return redirect('dealer_packages')

    stripe.api_key = stripe_secret_key

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
                + '/cars/payment-success/?session_id={CHECKOUT_SESSION_ID}'
            ),
            cancel_url=(
                settings.SITE_URL
                + '/cars/payment-cancelled/'
            ),
            metadata={
                'user_id': request.user.id,
                'package_name': package.name,
            },
            subscription_data={
                'metadata': {
                    'user_id': request.user.id,
                    'package_name': package.name,
                }
            }
        )

        PaymentTransaction.objects.update_or_create(
            transaction_id=checkout_session.id,
            defaults={
                'user': request.user,
                'amount': package.monthly_price,
                'package_name': package.name,
                'payment_status': 'pending',
            }
        )

        return redirect(checkout_session.url)

    except Exception as error:
        messages.error(
            request,
            f'Payment session could not be created: {error}'
        )

        return redirect('dealer_packages')


# ==========================================
# SECTION 06: PAYMENT SUCCESS
# ==========================================

@login_required
def payment_success(request):
    site_settings = get_site_settings()
    session_id = request.GET.get('session_id')
    stripe_secret_key = get_stripe_secret_key()

    if not session_id:
        messages.error(request, 'Payment session was missing.')
        return redirect('dealer_packages')

    if not stripe_secret_key:
        messages.error(request, 'Stripe payment is not configured yet.')
        return redirect('dealer_packages')

    stripe.api_key = stripe_secret_key

    try:
        checkout_session = stripe.checkout.Session.retrieve(
            session_id
        )

        if checkout_session.payment_status == 'paid':
            metadata_user_id = checkout_session.metadata.get('user_id')
            package_name = checkout_session.metadata.get('package_name')

            if (
                metadata_user_id
                and int(metadata_user_id) == request.user.id
                and get_dealer_package(package_name)
            ):
                activate_dealer_package(
                    user=request.user,
                    package_name=package_name,
                    stripe_session=checkout_session
                )

        if site_settings and site_settings.payment_success_message:
            messages.success(
                request,
                site_settings.payment_success_message
            )

        return render(
            request,
            'vehicles/payments/payment_success.html'
        )

    except Exception as error:
        messages.error(
            request,
            f'Payment verification failed: {error}'
        )

        return redirect('dealer_packages')


# ==========================================
# SECTION 07: PAYMENT CANCELLED
# ==========================================

@login_required
def payment_cancelled(request):
    site_settings = get_site_settings()

    if site_settings and site_settings.payment_cancelled_message:
        messages.warning(
            request,
            site_settings.payment_cancelled_message
        )

    return render(
        request,
        'vehicles/payments/payment_cancelled.html'
    )


# ==========================================
# SECTION 08: STRIPE WEBHOOK
# ==========================================

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    signature_header = request.META.get(
        'HTTP_STRIPE_SIGNATURE'
    )

    webhook_secret = get_stripe_webhook_secret()

    if not webhook_secret:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature_header,
            webhook_secret
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

            if user_id and get_dealer_package(package_name):
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

        deactivate_dealer_package_by_subscription(
            stripe_subscription_id
        )

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

            try:
                send_payment_failed_email(subscription.user)
            except Exception:
                pass

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