# ==========================================
# MyCarMarket
# Version: v1.5.2
# File: core/models.py
# Description: Site Settings + Ads + Stripe Payment Admin Settings + Validation
# ==========================================

from django.core.exceptions import ValidationError
from django.db import models


class SiteSettings(models.Model):

    # ==========================================
    # SECTION 01: CHOICES
    # ==========================================

    AD_TYPE_CHOICES = [
        ('custom', 'Custom Image Ad'),
        ('google', 'Google AdSense Ad'),
    ]

    STRIPE_MODE_CHOICES = [
        ('test', 'Test Mode'),
        ('live', 'Live Mode'),
    ]

    # ==========================================
    # SECTION 02: HOMEPAGE HERO
    # ==========================================

    hero_image = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True
    )

    hero_title = models.CharField(
        max_length=200,
        blank=True
    )

    hero_subtitle = models.CharField(
        max_length=300,
        blank=True
    )

    # ==========================================
    # SECTION 03: HOMEPAGE ADS
    # ==========================================

    homepage_ad_type = models.CharField(
        max_length=20,
        choices=AD_TYPE_CHOICES,
        default='custom'
    )

    alternate_google_banner_ad = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True
    )

    alternate_google_banner_link = models.URLField(
        blank=True
    )

    google_adsense_publisher_id = models.CharField(
        max_length=100,
        blank=True,
        help_text='Example: ca-pub-1234567890123456'
    )

    google_adsense_slot_id = models.CharField(
        max_length=100,
        blank=True,
        help_text='Homepage banner slot ID.'
    )

    # ==========================================
    # SECTION 04: CAR DETAIL ADS
    # ==========================================

    car_detail_sidebar_google_ad_active = models.BooleanField(
        default=False
    )

    car_detail_sidebar_google_slot_id = models.CharField(
        max_length=100,
        blank=True
    )

    # ==========================================
    # SECTION 05: STRIPE MAIN SETTINGS
    # ==========================================

    stripe_enabled = models.BooleanField(
        default=False,
        help_text='Enable or disable Stripe payments.'
    )

    stripe_mode = models.CharField(
        max_length=10,
        choices=STRIPE_MODE_CHOICES,
        default='test'
    )

    stripe_publishable_key = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe publishable key. Example: pk_test_... or pk_live_...'
    )

    stripe_secret_key = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe secret key. Example: sk_test_... or sk_live_...'
    )

    stripe_webhook_secret = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe webhook secret. Example: whsec_...'
    )

    # ==========================================
    # SECTION 06: STRIPE PRICE IDS
    # ==========================================

    stripe_price_starter = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe Price ID for Starter package.'
    )

    stripe_price_professional = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe Price ID for Professional package.'
    )

    stripe_price_premium = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe Price ID for Premium package.'
    )

    stripe_price_enterprise = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe Price ID for Enterprise package.'
    )

    # ==========================================
    # SECTION 07: PAYMENT MESSAGES
    # ==========================================

    payment_success_message = models.TextField(
        blank=True,
        default='Payment successful. Your dealer package is now active.'
    )

    payment_cancelled_message = models.TextField(
        blank=True,
        default='Payment was cancelled. You have not been charged.'
    )

    # ==========================================
    # SECTION 08: VALIDATION
    # ==========================================

    def clean(self):
        super().clean()

        errors = {}

        if self.stripe_enabled:

            required_fields = {
                'stripe_publishable_key': self.stripe_publishable_key,
                'stripe_secret_key': self.stripe_secret_key,
                'stripe_webhook_secret': self.stripe_webhook_secret,
                'stripe_price_starter': self.stripe_price_starter,
                'stripe_price_professional': self.stripe_price_professional,
                'stripe_price_premium': self.stripe_price_premium,
                'stripe_price_enterprise': self.stripe_price_enterprise,
            }

            for field_name, field_value in required_fields.items():
                if not field_value:
                    errors[field_name] = (
                        'This field is required when Stripe is enabled.'
                    )

            if (
                self.stripe_mode == 'test'
                and self.stripe_publishable_key
                and not self.stripe_publishable_key.startswith('pk_test_')
            ):
                errors['stripe_publishable_key'] = (
                    'Test mode requires a publishable key starting with pk_test_.'
                )

            if (
                self.stripe_mode == 'test'
                and self.stripe_secret_key
                and not self.stripe_secret_key.startswith('sk_test_')
            ):
                errors['stripe_secret_key'] = (
                    'Test mode requires a secret key starting with sk_test_.'
                )

            if (
                self.stripe_mode == 'live'
                and self.stripe_publishable_key
                and not self.stripe_publishable_key.startswith('pk_live_')
            ):
                errors['stripe_publishable_key'] = (
                    'Live mode requires a publishable key starting with pk_live_.'
                )

            if (
                self.stripe_mode == 'live'
                and self.stripe_secret_key
                and not self.stripe_secret_key.startswith('sk_live_')
            ):
                errors['stripe_secret_key'] = (
                    'Live mode requires a secret key starting with sk_live_.'
                )

            if (
                self.stripe_webhook_secret
                and not self.stripe_webhook_secret.startswith('whsec_')
            ):
                errors['stripe_webhook_secret'] = (
                    'Webhook secret must start with whsec_.'
                )

            stripe_price_fields = {
                'stripe_price_starter': self.stripe_price_starter,
                'stripe_price_professional': self.stripe_price_professional,
                'stripe_price_premium': self.stripe_price_premium,
                'stripe_price_enterprise': self.stripe_price_enterprise,
            }

            for field_name, field_value in stripe_price_fields.items():
                if field_value and not field_value.startswith('price_'):
                    errors[field_name] = (
                        'Stripe Price ID must start with price_.'
                    )

        if errors:
            raise ValidationError(errors)

    # ==========================================
    # SECTION 09: DISPLAY
    # ==========================================

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"