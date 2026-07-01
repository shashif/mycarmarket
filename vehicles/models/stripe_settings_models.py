# ==========================================
# MyCarMarket
# Version: v1.4.8
# File: vehicles/models/stripe_settings_models.py
# Description: Stripe Credentials Controlled From Django Admin
# ==========================================

from django.db import models


class StripeSettings(models.Model):

    is_enabled = models.BooleanField(
        default=False,
        help_text='Enable or disable Stripe payments.'
    )

    test_mode = models.BooleanField(
        default=True,
        help_text='Turn off only when using live Stripe keys.'
    )

    publishable_key = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe publishable key. Example: pk_test_... or pk_live_...'
    )

    secret_key = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe secret key. Example: sk_test_... or sk_live_...'
    )

    webhook_secret = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe webhook secret. Example: whsec_...'
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Stripe Settings'
        verbose_name_plural = 'Stripe Settings'

    def __str__(self):
        if self.test_mode:
            return 'Stripe Settings - Test Mode'
        return 'Stripe Settings - Live Mode'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj