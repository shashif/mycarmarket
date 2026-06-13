# ==========================================
# MyCarMarket
# Version: v0.9.4
# File: vehicles/admin/car_admin.py
# Car Admin
# ==========================================

from django.contrib import admin

from vehicles.models import Car
from .car_image_admin import CarImageInline


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'posted_by',
        'dealer_business',
        'dealer_package',
        'dealer_verified',
        'featured_dealer',
        'make',
        'model',
        'year',
        'price',
        'state',
        'suburb',
        'is_approved',
        'is_featured',
        'is_active',
        'is_verified_listing',
        'views_count',
    )

    list_editable = (
        'is_approved',
        'is_featured',
        'is_active',
        'is_verified_listing',
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
        'seller__email',
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
        'mark_as_featured',
        'remove_featured',
        'mark_as_verified_listing',
        'remove_verified_listing',
    )

    inlines = [CarImageInline]

    def posted_by(self, obj):
        if obj.seller:
            return obj.seller.username
        return "No User"

    posted_by.short_description = "Posted User"

    def dealer_business(self, obj):
        if obj.seller and hasattr(obj.seller, 'dealer_profile'):
            profile = obj.seller.dealer_profile
            return profile.business_name or obj.seller.username
        return "Private Seller"

    dealer_business.short_description = "Dealer Business"

    def dealer_package(self, obj):
        if obj.seller and hasattr(obj.seller, 'dealer_profile'):
            return obj.seller.dealer_profile.package_badge()
        return "Private Seller"

    dealer_package.short_description = "Package"

    def dealer_verified(self, obj):
        if obj.seller and hasattr(obj.seller, 'dealer_profile'):
            if obj.seller.dealer_profile.is_verified:
                return "✔ Verified"
        return "Not Verified"

    dealer_verified.short_description = "Dealer Verified"

    def featured_dealer(self, obj):
        if obj.seller and hasattr(obj.seller, 'dealer_profile'):
            if obj.seller.dealer_profile.is_featured_dealer:
                return "⭐ Featured"
        return "No"

    featured_dealer.short_description = "Featured Dealer"

    def approve_selected_listings(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, 'Selected listings approved successfully.')

    approve_selected_listings.short_description = "Approve selected listings"

    def unapprove_selected_listings(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, 'Selected listings moved to pending successfully.')

    unapprove_selected_listings.short_description = "Move selected listings to pending"

    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, 'Selected listings marked as featured.')

    mark_as_featured.short_description = "Mark selected listings as featured"

    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, 'Selected listings removed from featured.')

    remove_featured.short_description = "Remove selected listings from featured"

    def mark_as_verified_listing(self, request, queryset):
        queryset.update(is_verified_listing=True)
        self.message_user(request, 'Selected listings marked as verified.')

    mark_as_verified_listing.short_description = "Mark selected listings as verified"

    def remove_verified_listing(self, request, queryset):
        queryset.update(is_verified_listing=False)
        self.message_user(request, 'Selected listings removed from verified.')

    remove_verified_listing.short_description = "Remove selected listings from verified"