# ==========================================
# MyCarMarket
# Version: v1.5.0
# File: vehicles/models/dealer_models.py
# Description: Dealer Profile + Admin Editable Dealer Packages
# ==========================================

from django.db import models
from django.contrib.auth.models import User


# ==========================================
# SECTION 01: DEALER PACKAGE MODEL
# START
# ==========================================

class DealerPackage(models.Model):

    PACKAGE_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField(
        max_length=20,
        choices=PACKAGE_CHOICES,
        unique=True
    )

    display_name = models.CharField(
        max_length=100
    )

    monthly_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    max_listings = models.PositiveIntegerField(
        default=3
    )

    featured_ads_allowed = models.PositiveIntegerField(
        default=0
    )

    is_featured_dealer = models.BooleanField(
        default=False
    )

    priority_support = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    sort_order = models.PositiveIntegerField(
        default=0
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'sort_order',
            'monthly_price',
        ]

    def __str__(self):
        return f"{self.display_name} - ${self.monthly_price} AUD"


# ==========================================
# SECTION 01: DEALER PACKAGE MODEL
# END
# ==========================================


# ==========================================
# SECTION 02: DEALER PROFILE MODEL
# START
# ==========================================

class DealerProfile(models.Model):

    PACKAGE_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    BANNER_POSITION_CHOICES = [
        ('top', 'Top'),
        ('center', 'Center'),
        ('bottom', 'Bottom'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dealer_profile'
    )

    business_name = models.CharField(max_length=150, blank=True)
    business_description = models.TextField(blank=True)
    business_slogan = models.CharField(max_length=160, blank=True)
    years_in_business = models.PositiveIntegerField(default=0)
    dealer_owner_name = models.CharField(max_length=120, blank=True)

    dealer_owner_title = models.CharField(
        max_length=120,
        blank=True,
        default='Dealer Principal'
    )

    dealer_owner_photo = models.ImageField(
        upload_to='dealer_owner_photos/',
        blank=True,
        null=True
    )

    google_maps_link = models.URLField(blank=True)

    logo = models.ImageField(
        upload_to='dealer_logos/',
        blank=True,
        null=True
    )

    banner = models.ImageField(
        upload_to='dealer_banners/',
        blank=True,
        null=True
    )

    banner_position = models.CharField(
        max_length=20,
        choices=BANNER_POSITION_CHOICES,
        default='center'
    )

    website = models.URLField(blank=True)
    business_phone = models.CharField(max_length=30, blank=True)
    business_email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    abn = models.CharField(max_length=30, blank=True)
    opening_hours = models.CharField(max_length=255, blank=True)

    monday_hours = models.CharField(
        max_length=100,
        blank=True,
        default='9:00 AM - 5:00 PM'
    )

    tuesday_hours = models.CharField(
        max_length=100,
        blank=True,
        default='9:00 AM - 5:00 PM'
    )

    wednesday_hours = models.CharField(
        max_length=100,
        blank=True,
        default='9:00 AM - 5:00 PM'
    )

    thursday_hours = models.CharField(
        max_length=100,
        blank=True,
        default='9:00 AM - 5:00 PM'
    )

    friday_hours = models.CharField(
        max_length=100,
        blank=True,
        default='9:00 AM - 5:00 PM'
    )

    saturday_hours = models.CharField(
        max_length=100,
        blank=True,
        default='Closed'
    )

    sunday_hours = models.CharField(
        max_length=100,
        blank=True,
        default='Closed'
    )

    open_24_hours = models.BooleanField(default=False)

    monday_closed = models.BooleanField(default=False)
    monday_open_time = models.TimeField(null=True, blank=True)
    monday_close_time = models.TimeField(null=True, blank=True)

    tuesday_closed = models.BooleanField(default=False)
    tuesday_open_time = models.TimeField(null=True, blank=True)
    tuesday_close_time = models.TimeField(null=True, blank=True)

    wednesday_closed = models.BooleanField(default=False)
    wednesday_open_time = models.TimeField(null=True, blank=True)
    wednesday_close_time = models.TimeField(null=True, blank=True)

    thursday_closed = models.BooleanField(default=False)
    thursday_open_time = models.TimeField(null=True, blank=True)
    thursday_close_time = models.TimeField(null=True, blank=True)

    friday_closed = models.BooleanField(default=False)
    friday_open_time = models.TimeField(null=True, blank=True)
    friday_close_time = models.TimeField(null=True, blank=True)

    saturday_closed = models.BooleanField(default=True)
    saturday_open_time = models.TimeField(null=True, blank=True)
    saturday_close_time = models.TimeField(null=True, blank=True)

    sunday_closed = models.BooleanField(default=True)
    sunday_open_time = models.TimeField(null=True, blank=True)
    sunday_close_time = models.TimeField(null=True, blank=True)

    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    show_email = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=True)

    finance_available = models.BooleanField(default=False)
    trade_in_available = models.BooleanField(default=False)
    extended_warranty = models.BooleanField(default=False)
    delivery_available = models.BooleanField(default=False)
    test_drive_available = models.BooleanField(default=False)

    package = models.CharField(
        max_length=20,
        choices=PACKAGE_CHOICES,
        default='free'
    )

    is_dealer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    package_active = models.BooleanField(default=True)

    package_expiry = models.DateTimeField(
        null=True,
        blank=True
    )

    is_featured_dealer = models.BooleanField(default=False)
    max_listings = models.PositiveIntegerField(default=3)
    featured_ads_allowed = models.PositiveIntegerField(default=0)
    priority_support = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def package_badge(self):

        if self.package == 'enterprise':
            return '👑 Enterprise Dealer'

        if self.package == 'premium':
            return '⭐ Premium Dealer'

        if self.package == 'professional':
            return '🏢 Professional Dealer'

        if self.package == 'starter':
            return '🚗 Starter Dealer'

        return 'Basic Seller'

    def verified_badge(self):

        if self.is_verified:
            return '✔ Verified Dealer'

        return ''

    def format_day_hours(self, is_closed, open_time, close_time):

        if self.open_24_hours:
            return 'Open 24 Hours'

        if is_closed:
            return 'Closed'

        if open_time and close_time:
            return (
                f"{open_time.strftime('%I:%M %p')} - "
                f"{close_time.strftime('%I:%M %p')}"
            )

        return 'Not set'

    def monday_display_hours(self):
        return self.format_day_hours(
            self.monday_closed,
            self.monday_open_time,
            self.monday_close_time
        )

    def tuesday_display_hours(self):
        return self.format_day_hours(
            self.tuesday_closed,
            self.tuesday_open_time,
            self.tuesday_close_time
        )

    def wednesday_display_hours(self):
        return self.format_day_hours(
            self.wednesday_closed,
            self.wednesday_open_time,
            self.wednesday_close_time
        )

    def thursday_display_hours(self):
        return self.format_day_hours(
            self.thursday_closed,
            self.thursday_open_time,
            self.thursday_close_time
        )

    def friday_display_hours(self):
        return self.format_day_hours(
            self.friday_closed,
            self.friday_open_time,
            self.friday_close_time
        )

    def saturday_display_hours(self):
        return self.format_day_hours(
            self.saturday_closed,
            self.saturday_open_time,
            self.saturday_close_time
        )

    def sunday_display_hours(self):
        return self.format_day_hours(
            self.sunday_closed,
            self.sunday_open_time,
            self.sunday_close_time
        )

    def __str__(self):

        name = self.business_name or self.user.username

        return f"{name} - {self.package}"


# ==========================================
# SECTION 02: DEALER PROFILE MODEL
# END
# ==========================================


# ==========================================
# END FILE
# ==========================================