# ==========================================
# MyCarMarket Australia
# Version: v2.0.0
# File: rentals/apps.py
# Description:
# Rentals application configuration.
# ==========================================

from django.apps import AppConfig


# ==========================================
# SECTION 1 START
# App Configuration
# ==========================================

class RentalsConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"

    name = "rentals"

    verbose_name = "Rental Cars"


# ==========================================
# SECTION 1 END
# App Configuration
# ==========================================