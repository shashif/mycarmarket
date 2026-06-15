# ==========================================
# MyCarMarket
# Version: v1.0.9
# File: vehicles/models/payment_models.py
# Dealer Subscription + Payment Transaction
# ==========================================

from django.db import models
from django.contrib.auth.models import User


class DealerSubscription(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dealer_subscription'
    )

    package_name = models.CharField(max_length=50)

    monthly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    started_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True
    )

    stripe_subscription_id = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.package_name}"


class PaymentTransaction(models.Model):

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    package_name = models.CharField(max_length=50)

    transaction_id = models.CharField(
        max_length=255,
        unique=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.amount}"