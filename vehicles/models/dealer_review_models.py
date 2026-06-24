# ==========================================
# MyCarMarket
# Version: v1.4.0
# File: vehicles/models/dealer_review_models.py
# Dealer Reviews Model
# ==========================================

from django.db import models
from django.contrib.auth.models import User


class DealerReview(models.Model):

    dealer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dealer_reviews'
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_dealer_reviews'
    )

    rating = models.PositiveSmallIntegerField(
        default=5
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = (
            'dealer',
            'reviewer',
        )

        ordering = [
            '-created_at'
        ]

    def __str__(self):
        return f'{self.dealer.username} - {self.rating} stars'