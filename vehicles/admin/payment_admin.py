# ==========================================
# MyCarMarket
# Version: v1.0.9
# File: vehicles/admin/payment_admin.py
# Payment Admin
# ==========================================

from django.contrib import admin

from vehicles.models import (
    DealerSubscription,
    PaymentTransaction
)


@admin.register(DealerSubscription)
class DealerSubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'package_name',
        'monthly_price',
        'status',
        'started_at',
        'expires_at',
    )

    search_fields = (
        'user__username',
        'package_name',
    )


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'amount',
        'package_name',
        'payment_status',
        'created_at',
    )

    search_fields = (
        'user__username',
        'transaction_id',
    )