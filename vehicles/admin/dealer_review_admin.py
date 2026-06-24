# ==========================================
# MyCarMarket
# Version: v1.4.0
# File: vehicles/admin/dealer_review_admin.py
# Dealer Review Admin
# ==========================================

from django.contrib import admin

from vehicles.models import DealerReview


@admin.register(DealerReview)
class DealerReviewAdmin(admin.ModelAdmin):

    list_display = (
        'dealer',
        'reviewer',
        'rating',
        'created_at',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    search_fields = (
        'dealer__username',
        'dealer__email',
        'reviewer__username',
        'reviewer__email',
        'comment',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )