# ==========================================
# MyCarMarket
# Version: v1.2.3
# File: vehicles/models/enquiry_models.py
# Dealer Enquiry System Upgrade
# ==========================================

from django.db import models


class Enquiry(models.Model):

    # ==========================================
    # Dealer Owner
    # NOTE:
    # null=True and blank=True are important because
    # old enquiries may already exist in your database.
    # After all old data is clean, we can make this required later.
    # ==========================================

    dealer = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='dealer_enquiries',
        null=True,
        blank=True
    )

    # ==========================================
    # Car Related To This Enquiry
    # ==========================================

    car = models.ForeignKey(
        'vehicles.Car',
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    # ==========================================
    # Buyer Details
    # ==========================================

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30
    )

    message = models.TextField()

    # ==========================================
    # Enquiry Status
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    class Meta:

        verbose_name_plural = 'Enquiries'

        ordering = [
            '-created_at'
        ]

    def __str__(self):

        return (
            f"{self.name} - "
            f"{self.car.title}"
        )


# ==========================================
# END ENQUIRY MODEL
# ==========================================