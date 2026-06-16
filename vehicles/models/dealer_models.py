# ==========================================
# MyCarMarket
# Version: v1.1.9
# File: vehicles/models/dealer_models.py
# Dealer Profile Model + Cover Photo Position
# ==========================================

from django.db import models
from django.contrib.auth.models import User


class DealerProfile(models.Model):

    PACKAGE_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter - $99 AUD'),
        ('professional', 'Professional - $299 AUD'),
        ('premium', 'Premium - $599 AUD'),
        ('enterprise', 'Enterprise - $999 AUD'),
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

    logo = models.ImageField(upload_to='dealer_logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='dealer_banners/', blank=True, null=True)

    banner_position = models.CharField(
        max_length=20,
        choices=BANNER_POSITION_CHOICES,
        default='center'
    )

    website = models.URLField(blank=True)
    business_phone = models.CharField(max_length=30, blank=True)
    business_email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)

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

    def __str__(self):

        name = self.business_name or self.user.username

        return f"{name} - {self.package}"


# ==========================================
# END DEALER PROFILE MODEL
# ==========================================