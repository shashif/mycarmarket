# ==========================================
# MyCarMarket
# Version: v1.5.0
# File: vehicles/admin/package_admin.py
# Description: Admin Editable Dealer Packages
# ==========================================

from django.contrib import admin

from vehicles.models import DealerPackage


@admin.register(DealerPackage)
class DealerPackageAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'display_name',
        'monthly_price',
        'max_listings',
        'featured_ads_allowed',
        'is_featured_dealer',
        'priority_support',
        'is_active',
        'sort_order',
    )

    list_editable = (
        'monthly_price',
        'max_listings',
        'featured_ads_allowed',
        'is_featured_dealer',
        'priority_support',
        'is_active',
        'sort_order',
    )

    list_filter = (
        'is_active',
        'is_featured_dealer',
        'priority_support',
    )

    search_fields = (
        'name',
        'display_name',
    )

    ordering = (
        'sort_order',
        'monthly_price',
    )