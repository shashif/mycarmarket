# ==========================================
# MyCarMarket
# Version: v0.9.4
# File: vehicles/admin/favourite_admin.py
# Favourite Car Admin
# ==========================================

from django.contrib import admin

from vehicles.models import FavouriteCar


@admin.register(FavouriteCar)
class FavouriteCarAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'car',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'car__title',
        'car__make',
        'car__model',
    )

    readonly_fields = (
        'created_at',
    )