# ==========================================
# MyCarMarket Australia
# Version: v2.3.0
# File: core/urls.py
# Location: core/urls.py
# Description:
# Core URLs
# Homepage + Static Pages + Global Moderation Center
# Last Updated: 24 Jul 2026
# ==========================================

from django.urls import path

from .views import (
    home,
    sell_car,
    dealers,
    terms_conditions,
    privacy_policy,
    contact_us,
    moderation_center,
    moderation_action,
)

urlpatterns = [

    # ==========================================
    # HOME
    # ==========================================

    path(
        "",
        home,
        name="home",
    ),

    # ==========================================
    # SELL CAR
    # ==========================================

    path(
        "sell-car/",
        sell_car,
        name="sell_car",
    ),

    # ==========================================
    # DEALERS
    # ==========================================

    path(
        "dealers/",
        dealers,
        name="dealers",
    ),

    # ==========================================
    # LEGAL
    # ==========================================

    path(
        "terms/",
        terms_conditions,
        name="terms_conditions",
    ),

    path(
        "privacy/",
        privacy_policy,
        name="privacy_policy",
    ),

    path(
        "contact/",
        contact_us,
        name="contact_us",
    ),

    # ==========================================
    # GLOBAL MODERATION CENTER
    # ==========================================

    path(
        "moderation/",
        moderation_center,
        name="moderation_center",
    ),

    path(
        "moderation/<str:listing_type>/<int:object_id>/<str:action>/",
        moderation_action,
        name="moderation_action",
    ),

]