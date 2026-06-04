# ==========================================
# MyCarMarket
# Version: v0.3.6 - Admin With Trust + Views
# File: vehicles/admin.py
# ==========================================

from django.contrib import admin
from .models import Car, CarImage, Enquiry


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

    fields = (
        'image',
        'is_primary',
        'sort_order',
    )


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Basic Car Information', {
            'fields': (
                'title',
                'make',
                'model',
                'year',
                'price',
                'kilometres',
            )
        }),

        ('Vehicle Details', {
            'fields': (
                'location',
                'transmission',
                'fuel_type',
                'body_type',
            )
        }),

        ('Seller Information - Private Admin Only', {
            'fields': (
                'seller_name',
                'seller_email',
                'seller_phone',
            )
        }),

        ('Marketplace Settings', {
            'fields': (
                'is_featured',
                'is_active',
                'is_verified_listing',
                'views_count',
            )
        }),

        ('Description', {
            'fields': (
                'description',
            )
        }),
    )

    readonly_fields = (
        'views_count',
    )

    list_display = (
        'title',
        'make',
        'model',
        'year',
        'price',
        'body_type',
        'location',
        'views_count',
        'is_verified_listing',
        'is_featured',
        'is_active',
    )

    list_filter = (
        'make',
        'year',
        'body_type',
        'transmission',
        'fuel_type',
        'is_verified_listing',
        'is_featured',
        'is_active',
    )

    search_fields = (
        'title',
        'make',
        'model',
        'location',
        'body_type',
        'seller_name',
        'seller_email',
        'seller_phone',
    )

    inlines = [CarImageInline]


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = (
        'car',
        'is_primary',
        'sort_order',
    )

    list_filter = (
        'is_primary',
    )


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'car',
        'is_read',
        'created_at',
    )

    list_filter = (
        'is_read',
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'phone',
        'message',
        'car__title',
    )

    readonly_fields = (
        'car',
        'name',
        'email',
        'phone',
        'message',
        'created_at',
    )