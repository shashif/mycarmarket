# ==========================================
# MyCarMarket
# Version: v0.7.1
# File: accounts/models.py
# User Profile + Dealer Account Type
# ==========================================

from django.db import models
from django.contrib.auth.models import User


ACCOUNT_TYPE_CHOICES = [
    ('normal', 'Normal User'),
    ('dealer', 'Dealer'),
]


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default='normal'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    business_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_type}"