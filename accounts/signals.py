# ==========================================
# MyCarMarket
# Version: v0.7.1
# File: accounts/signals.py
# Auto Create Profile For Every User
# ==========================================

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

    if hasattr(instance, 'profile'):
        instance.profile.save()