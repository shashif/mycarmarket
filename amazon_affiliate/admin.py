# ==========================================
# MyCarMarket
# Version: v1.15.0
# File: amazon_affiliate/admin.py
# Description:
# Amazon Accessories Store Admin
# One Global Store ID in Settings Only
# Clean Product Admin Form
# ==========================================

from django.contrib import admin

from .models import (
    AmazonAffiliateSettings,
    AmazonCategory,
    AmazonProduct,
)


@admin.register(AmazonAffiliateSettings)
class AmazonAffiliateSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "store_id",
        "is_active",
        "updated_at",
    )

    list_editable = (
        "is_active",
    )


@admin.register(AmazonCategory)
class AmazonCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "is_active",
        "display_order",
    )

    list_editable = (
        "is_active",
        "display_order",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    search_fields = (
        "name",
        "short_description",
    )


@admin.register(AmazonProduct)
class AmazonProductAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "product_category",
        "body_type",
        "asin",
        "is_featured",
        "is_active",
        "display_order",
        "click_count",
    )

    list_filter = (
        "product_category",
        "body_type",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "title",
        "asin",
        "amazon_product_url",
        "amazon_affiliate_url",
    )

    list_editable = (
        "is_featured",
        "is_active",
        "display_order",
    )

    readonly_fields = (
        "asin",
        "amazon_affiliate_url",
        "click_count",
        "last_synced_at",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Amazon Product Link", {
            "fields": (
                "amazon_product_url",
                "asin",
                "amazon_affiliate_url",
            )
        }),
        ("Product Details", {
            "fields": (
                "title",
                "product_category",
                "body_type",
                "image",
            )
        }),
        ("Display Settings", {
            "fields": (
                "button_text",
                "is_active",
                "is_featured",
                "display_order",
            )
        }),
        ("Tracking", {
            "fields": (
                "click_count",
                "last_synced_at",
                "created_at",
                "updated_at",
            )
        }),
    )