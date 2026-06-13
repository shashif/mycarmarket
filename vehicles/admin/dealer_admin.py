# ==========================================
# MyCarMarket
# Version: v0.9.4
# File: vehicles/admin/dealer_admin.py
# Dealer Profile Admin
# ==========================================

from django.contrib import admin
from django.utils.html import format_html

from vehicles.models import DealerProfile


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