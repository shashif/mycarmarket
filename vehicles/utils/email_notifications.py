# ==========================================
# MyCarMarket
# Version: v1.8.1
# File: vehicles/utils/email_notifications.py
# Description:
# Email notification helpers for car listings.
#
# Sends email when:
# 1. User submits a new listing (Pending Approval)
# 2. Admin approves the listing
# ==========================================

from django.conf import settings
from django.core.mail import send_mail


# ==========================================
# LISTING PENDING EMAIL
# ==========================================

def send_listing_pending_email(car):
    """
    Send email after user submits a new car listing.
    """

    if not car.posted_by:
        return

    if not car.posted_by.email:
        return

    subject = "We've received your car listing - MyCarMarket Australia"

    message = f"""
Hi {car.posted_by.get_full_name() or car.posted_by.username},

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
        recipient_list=[car.posted_by.email],
        fail_silently=True,
    )


# ==========================================
# LISTING APPROVED EMAIL
# ==========================================

def send_listing_approved_email(car):
    """
    Send email after admin approves a car listing.
    """

    if not car.posted_by:
        return

    if not car.posted_by.email:
        return

    subject = "Your car listing has been approved! - MyCarMarket Australia"

    message = f"""
Hi {car.posted_by.get_full_name() or car.posted_by.username},

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
        recipient_list=[car.posted_by.email],
        fail_silently=True,
    )