# ==========================================
# MyCarMarket
# Version: v0.8.6 FIXED
# File: vehicles/admin.py
# Admin Seller Username + Quick Approval + Dealer Branding + Dealer Packages
# ==========================================

from django.contrib import admin
from django.utils.html import format_html

from .models import Car, CarImage, Enquiry, FavouriteCar, DealerProfile


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


@admin.register(DealerProfile)
class DealerProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'business_name',
        'logo_preview',
        'package',
        'is_dealer',
        'is_verified',
        'is_featured_dealer',
        'package_active',
        'max_listings',
        'featured_ads_allowed',
        'priority_support',
        'created_at',
    )

    list_editable = (
        'package',
        'is_dealer',
        'is_verified',
        'is_featured_dealer',
        'package_active',
        'max_listings',
        'featured_ads_allowed',
        'priority_support',
    )

    list_filter = (
        'package',
        'is_dealer',
        'is_verified',
        'is_featured_dealer',
        'package_active',
        'priority_support',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'business_name',
        'business_phone',
        'business_email',
        'address',
    )

    readonly_fields = (
        'logo_preview',
        'banner_preview',
        'created_at',
    )

    fields = (
        'user',
        'business_name',
        'business_description',
        'logo_preview',
        'logo',
        'banner_preview',
        'banner',
        'website',
        'business_phone',
        'business_email',
        'address',
        'package',
        'is_dealer',
        'is_verified',
        'is_featured_dealer',
        'package_active',
        'max_listings',
        'featured_ads_allowed',
        'priority_support',
        'created_at',
    )

    actions = (
        'mark_verified',
        'remove_verified',
        'mark_as_featured_dealer',
        'remove_featured_dealer',
        'activate_package',
        'deactivate_package',
    )

    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html(
                '<img src="{}" style="width:80px;height:80px;object-fit:cover;border-radius:50%;" />',
                obj.logo.url
            )
        return "No Logo"

    logo_preview.short_description = "Logo"

    def banner_preview(self, obj):
        if obj and obj.banner:
            return format_html(
                '<img src="{}" style="width:280px;height:90px;object-fit:cover;border-radius:10px;" />',
                obj.banner.url
            )
        return "No Banner"

    banner_preview.short_description = "Banner"

    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, 'Selected dealers marked as verified.')

    mark_verified.short_description = "Mark selected dealers as verified"

    def remove_verified(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, 'Selected dealers removed from verified.')

    remove_verified.short_description = "Remove selected dealers from verified"

    def mark_as_featured_dealer(self, request, queryset):
        queryset.update(is_featured_dealer=True)
        self.message_user(request, 'Selected dealers marked as featured.')

    mark_as_featured_dealer.short_description = "Mark selected dealers as featured"

    def remove_featured_dealer(self, request, queryset):
        queryset.update(is_featured_dealer=False)
        self.message_user(request, 'Selected dealers removed from featured.')

    remove_featured_dealer.short_description = "Remove selected dealers from featured"

    def activate_package(self, request, queryset):
        queryset.update(package_active=True)
        self.message_user(request, 'Selected dealer packages activated.')

    activate_package.short_description = "Activate selected packages"

    def deactivate_package(self, request, queryset):
        queryset.update(package_active=False)
        self.message_user(request, 'Selected dealer packages deactivated.')

    deactivate_package.short_description = "Deactivate selected packages"