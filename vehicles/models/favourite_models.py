# ==========================================
# MyCarMarket
# Version: v1.0.5
# File: vehicles/models/favourite_models.py
# Favourite Car Model
# ==========================================

from django.db import models
from django.contrib.auth.models import User


class FavouriteCar(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite_cars'
    )

    car = models.ForeignKey(
        'vehicles.Car',
        on_delete=models.CASCADE,
        related_name='favourited_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} saved {self.car.title}"


# ==========================================
# END FAVOURITE CAR MODEL
# ==========================================