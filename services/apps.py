# ==========================================
# MyCarMarket Australia
# Version: v2.2.0
# File: services/apps.py
# Description:
# Services application configuration
# ==========================================


# ==========================================
# SECTION 1 START
# Imports
# ==========================================

from django.apps import AppConfig

# ==========================================
# SECTION 1 END
# Imports
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 2 START
# Services App Configuration
# ==========================================

class ServicesConfig(AppConfig):

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = "services"

    verbose_name = (
        "Car Services"
    )

    def ready(self):

        """
        Reserved for future signals.
        """

        pass


# ==========================================
# SECTION 2 END
# Services App Configuration
# ==========================================