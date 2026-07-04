# ==========================================
# MyCarMarket
# Version: v1.9.6
# File: vehicles/utils/email_notifications.py
# Description:
# Email notification helpers for car listings.
#
# Sends email when:
# 1. User submits a new listing
# 2. Admin approves the listing
# ==========================================

from django.conf import settings
from django.core.mail import send_mail


def get_listing_owner(car):
    if hasattr(car, "posted_by") and car.posted_by:
        return car.posted_by

    if hasattr(car, "seller") and car.seller:
        return car.seller

    return None


def send_listing_pending_email(car):
    owner = get_listing_owner(car)

    if not owner or not owner.email:
        return False

    subject = "We've received your car listing - MyCarMarket Australia"

    message = f"""
Hi {owner.get_full_name() or owner.username},

Thank you for listing your vehicle on MyCarMarket Australia.

Your listing has been successfully submitted and is currently waiting for approval by our moderation team.

Listing Details
-----------------------
Title: {car.title}

What happens next?

• Our team will review your listing.
• Once approved, your vehicle will become visible on the website.
• You will receive another email confirming approval.

Thank you for choosing MyCarMarket Australia.

Kind regards,

MyCarMarket Australia
https://mycarmarket.com.au
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[owner.email],
        fail_silently=True,
    )

    return True


def send_listing_approved_email(car):
    owner = get_listing_owner(car)

    if not owner or not owner.email:
        return False

    subject = "Your car listing has been approved! - MyCarMarket Australia"

    message = f"""
Hi {owner.get_full_name() or owner.username},

Congratulations!

Your car listing has now been approved and is LIVE on MyCarMarket Australia.

Listing Details
-----------------------
Title: {car.title}

Buyers can now view your vehicle and contact you directly through the website.

Thank you for choosing MyCarMarket Australia.

We wish you the very best in selling your vehicle.

Kind regards,

MyCarMarket Australia
https://mycarmarket.com.au
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[owner.email],
        fail_silently=True,
    )

    return True