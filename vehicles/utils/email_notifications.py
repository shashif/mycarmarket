# ==========================================
# MyCarMarket
# Version: v1.9.9
# File: vehicles/utils/email_notifications.py
# Description:
# Email notification helpers for car listings.
#
# Sends email when:
# 1. User submits a new listing
# 2. Admin approves the listing
# 3. Admin rejects the listing
# 4. Admin suspends the listing
# 5. Admin receives new listing notification
# ==========================================

from django.conf import settings
from django.core.mail import send_mail


# ==========================================
# SECTION 01 START
# Get Listing Owner
# ==========================================

def get_listing_owner(car):
    if hasattr(car, "posted_by") and car.posted_by:
        return car.posted_by

    if hasattr(car, "seller") and car.seller:
        return car.seller

    return None

# ==========================================
# SECTION 01 END
# ==========================================


# ==========================================
# SECTION 02 START
# Safe Email Sender
# ==========================================

def safe_send_mail(subject, message, recipient_list):
    if not recipient_list:
        return False

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        return True

    except Exception:
        return False

# ==========================================
# SECTION 02 END
# ==========================================


# ==========================================
# SECTION 03 START
# Listing Pending Email To Seller
# ==========================================

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

    return safe_send_mail(
        subject=subject,
        message=message,
        recipient_list=[owner.email],
    )

# ==========================================
# SECTION 03 END
# ==========================================


# ==========================================
# SECTION 04 START
# Listing Approved Email To Seller
# ==========================================

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

    return safe_send_mail(
        subject=subject,
        message=message,
        recipient_list=[owner.email],
    )

# ==========================================
# SECTION 04 END
# ==========================================


# ==========================================
# SECTION 05 START
# Listing Rejected Email To Seller
# ==========================================

def send_listing_rejected_email(car):
    owner = get_listing_owner(car)

    if not owner or not owner.email:
        return False

    reason = getattr(car, "rejected_reason", "") or "No specific reason was provided."

    subject = "Your car listing was not approved - MyCarMarket Australia"

    message = f"""
Hi {owner.get_full_name() or owner.username},

Thank you for submitting your vehicle listing to MyCarMarket Australia.

Unfortunately, your listing was not approved at this time.

Listing Details
-----------------------
Title: {car.title}

Reason
-----------------------
{reason}

You may update your listing and submit it again if required.

Kind regards,

MyCarMarket Australia
https://mycarmarket.com.au
"""

    return safe_send_mail(
        subject=subject,
        message=message,
        recipient_list=[owner.email],
    )

# ==========================================
# SECTION 05 END
# ==========================================


# ==========================================
# SECTION 06 START
# Listing Suspended Email To Seller
# ==========================================

def send_listing_suspended_email(car):
    owner = get_listing_owner(car)

    if not owner or not owner.email:
        return False

    reason = getattr(car, "suspended_reason", "") or "No specific reason was provided."

    subject = "Your car listing has been suspended - MyCarMarket Australia"

    message = f"""
Hi {owner.get_full_name() or owner.username},

Your vehicle listing has been suspended by the MyCarMarket Australia moderation team.

Listing Details
-----------------------
Title: {car.title}

Reason
-----------------------
{reason}

If you believe this was a mistake, please contact our support team.

Kind regards,

MyCarMarket Australia
https://mycarmarket.com.au
"""

    return safe_send_mail(
        subject=subject,
        message=message,
        recipient_list=[owner.email],
    )

# ==========================================
# SECTION 06 END
# ==========================================


# ==========================================
# SECTION 07 START
# New Listing Admin Notification
# ==========================================

def send_new_listing_admin_email(car):
    admin_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)

    if not admin_email:
        return False

    owner = get_listing_owner(car)

    seller_name = "Unknown Seller"
    seller_email = "No email"

    if owner:
        seller_name = owner.get_full_name() or owner.username
        seller_email = owner.email or "No email"

    subject = "New car listing pending approval - MyCarMarket Australia"

    message = f"""
Hi Admin,

A new car listing has been submitted and is waiting for approval.

Listing Details
-----------------------
Title: {car.title}
Seller: {seller_name}
Seller Email: {seller_email}

Please review this listing in the admin dashboard.

MyCarMarket Australia
https://mycarmarket.com.au/admin/
"""

    return safe_send_mail(
        subject=subject,
        message=message,
        recipient_list=[admin_email],
    )

# ==========================================
# SECTION 07 END
# ==========================================


# ==========================================
# SECTION 08 START
# End File
# ==========================================

# ==========================================
# SECTION 08 END
# ==========================================