# ==========================================
# MyCarMarket
# Version: v1.1.7
# File: vehicles/models/enquiry_models.py
# Enquiry Model - Phone Number Required
# ==========================================

from django.db import models


class Enquiry(models.Model):

    car = models.ForeignKey(
        'vehicles.Car',
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
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