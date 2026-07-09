# ==========================================
# MyCarMarket
# Version: v1.14.1
# File: amazon_affiliate/admin.py
# Description:
# Amazon Accessories Store Admin
# Hide Product Affiliate URL
# Show Editable Store ID in Product Admin
# ==========================================

from django import forms
from django.contrib import admin

from .models import (
    AmazonAffiliateSettings,
    AmazonCategory,
    AmazonProduct,
)


# ==========================================
# SECTION 1 START
# AMAZON PRODUCT ADMIN FORM
# ==========================================

class AmazonProductAdminForm(forms.ModelForm):

    store_id = forms.CharField(
        max_length=100,
        required=False,
        label="Amazon Store ID / Tracking ID",
        help_text="Example: mycarmarketau-22. This will be used automatically for all product links."
    )

    class Meta:
        model = AmazonProduct
        fields = "__all__"

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        affiliate_settings = AmazonAffiliateSettings.objects.filter(
            is_active=True
        ).first()

        if affiliate_settings:
            self.fields["store_id"].initial = affiliate_settings.store_id


# ==========================================
# SECTION 1 END
# AMAZON PRODUCT ADMIN FORM
# ==========================================


# ==========================================
# SECTION 2 START
# AMAZON AFFILIATE SETTINGS ADMIN
# ==========================================

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


# ==========================================
# SECTION 2 END
# AMAZON AFFILIATE SETTINGS ADMIN
# ==========================================


# ==========================================
# SECTION 3 START
# AMAZON CATEGORY ADMIN
# ==========================================

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


# ==========================================
# SECTION 3 END
# AMAZON CATEGORY ADMIN
# ==========================================


# ==========================================
# SECTION 4 START
# AMAZON PRODUCT ADMIN
# ==========================================

@admin.register(AmazonProduct)
class AmazonProductAdmin(admin.ModelAdmin):

    form = AmazonProductAdminForm

    list_display = (
        "title",
        "brand",
        "product_category",
        "body_type",
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
        "brand",
        "asin",
        "amazon_product_url",
    )

    list_editable = (
        "is_featured",
        "is_active",
        "display_order",
    )

    readonly_fields = (
        "click_count",
        "last_synced_at",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Amazon Link", {
            "fields": (
                "amazon_product_url",
                "store_id",
                "asin",
            )
        }),
        ("Product Details", {
            "fields": (
                "title",
                "brand",
                "short_description",
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

    def save_model(self, request, obj, form, change):

        store_id = form.cleaned_data.get("store_id")

        if store_id:
            AmazonAffiliateSettings.objects.update_or_create(
                is_active=True,
                defaults={
                    "store_id": store_id,
                }
            )

        super().save_model(request, obj, form, change)


# ==========================================
# SECTION 4 END
# AMAZON PRODUCT ADMIN
# ==========================================