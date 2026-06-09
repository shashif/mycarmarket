# ==========================================
# MyCarMarket
# Version: v0.7.1
# File: accounts/admin.py
# Profile Admin - Normal User / Dealer Control
# ==========================================

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'account_type',
        'business_name',
        'phone',
        'created_at',
    )

    list_filter = (
        'account_type',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'business_name',
        'phone',
    )