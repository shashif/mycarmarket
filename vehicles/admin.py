# ==========================================
# MyCarMarket
# Version: v0.5.2
# File: vehicles/admin.py
# Admin Approval Added
# ==========================================

from django.contrib import admin
from django.utils.html import format_html
from .models import Car, CarImage, Enquiry


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

    fields = (
        'image_preview',
        'image',
        'is_primary',
        'sort_order',
    )

    readonly_fields = (
        'image_preview',
    )

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="width:120px;height:80px;object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'make',
        'model',
        'year',
        'price',
        'state',
        'suburb',
        'seller',
        'is_approved',
        'is_featured',
        'is_active',
        'is_verified_listing',
        'views_count',
    )

    list_filter = (
        'is_approved',
        'state',
        'make',
        'body_type',
        'fuel_type',
        'transmission',
        'seller',
        'is_featured',
        'is_active',
        'is_verified_listing',
    )

    search_fields = (
        'title',
        'make',
        'model',
        'suburb',
        'state',
        'seller_name',
        'seller_email',
        'seller_phone',
        'seller__username',
    )

    readonly_fields = (
        'views_count',
        'created_at',
    )

    fields = (
        'title',
        'make',
        'model',
        'year',
        'price',
        'kilometres',

        'body_type',
        'transmission',
        'fuel_type',

        'state',
        'suburb',

        'description',

        'seller_name',
        'seller_email',
        'seller_phone',

        'seller',

        'is_approved',
        'is_featured',
        'is_active',
        'is_verified_listing',

        'views_count',
        'created_at',
    )

    actions = (
        'approve_selected_listings',
        'unapprove_selected_listings',
    )

    inlines = [CarImageInline]

    def approve_selected_listings(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(
            request,
            'Selected listings approved successfully.'
        )

    approve_selected_listings.short_description = "Approve selected listings"

    def unapprove_selected_listings(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(
            request,
            'Selected listings moved to pending successfully.'
        )

    unapprove_selected_listings.short_description = "Move selected listings to pending"


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'car',
        'image_preview',
        'is_primary',
        'sort_order',
    )

    list_filter = (
        'is_primary',
    )

    search_fields = (
        'car__title',
        'car__make',
        'car__model',
    )

    readonly_fields = (
        'image_preview',
    )

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="width:120px;height:80px;object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'car',
        'name',
        'email',
        'phone',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'phone',
        'message',
        'car__title',
        'car__make',
        'car__model',
    )

    readonly_fields = (
        'created_at',
    )