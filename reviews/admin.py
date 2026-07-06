from django.contrib import admin

# Register your models here.
# ==========================================
# MyCarMarket
# Version: v1.10.3
# File: reviews/admin.py
# Description: Car Review Admin
# ==========================================

from django.contrib import admin

from .models import CarReview


# ==========================================
# SECTION 01: CAR REVIEW ADMIN
# START
# ==========================================

@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'make',
        'model',
        'year',
        'rating',
        'is_featured',
        'is_published',
        'published_at',
    )

    list_filter = (
        'make',
        'is_featured',
        'is_published',
        'year',
    )

    search_fields = (
        'title',
        'make',
        'model',
        'summary',
    )

    list_editable = (
        'is_featured',
        'is_published',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    ordering = (
        '-published_at',
    )


# ==========================================
# SECTION 01: CAR REVIEW ADMIN
# END
# ==========================================