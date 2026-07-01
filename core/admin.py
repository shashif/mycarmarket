# ==========================================
# MyCarMarket
# Version: v1.5.1
# File: core/admin.py
# Description: Site Settings Admin + Ads + Stripe Payment Settings
# ==========================================

from django.contrib import admin
from django.utils.html import format_html

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    readonly_fields = (
        'hero_image_preview',
        'alternate_banner_preview',
    )

    fieldsets = (
        (
            'Homepage Hero Banner',
            {
                'fields': (
                    'hero_image',
                    'hero_image_preview',
                    'hero_title',
                    'hero_subtitle',
                )
            }
        ),
        (
            'Homepage Advertisement',
            {
                'fields': (
                    'homepage_ad_type',
                    'alternate_google_banner_ad',
                    'alternate_banner_preview',
                    'alternate_google_banner_link',
                    'google_adsense_publisher_id',
                    'google_adsense_slot_id',
                )
            }
        ),
        (
            'Car Detail Sidebar Advertisement',
            {
                'fields': (
                    'car_detail_sidebar_google_ad_active',
                    'car_detail_sidebar_google_slot_id',
                )
            }
        ),
        (
            'Stripe Main Settings',
            {
                'fields': (
                    'stripe_enabled',
                    'stripe_mode',
                    'stripe_publishable_key',
                    'stripe_secret_key',
                    'stripe_webhook_secret',
                )
            }
        ),
        (
            'Stripe Package Price IDs',
            {
                'fields': (
                    'stripe_price_starter',
                    'stripe_price_professional',
                    'stripe_price_premium',
                    'stripe_price_enterprise',
                )
            }
        ),
        (
            'Payment Messages',
            {
                'fields': (
                    'payment_success_message',
                    'payment_cancelled_message',
                )
            }
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def hero_image_preview(self, obj):
        if obj and obj.hero_image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:10px;">',
                obj.hero_image.url
            )

        return "No Hero Image"

    hero_image_preview.short_description = "Current Hero Image"

    def alternate_banner_preview(self, obj):
        if obj and obj.alternate_google_banner_ad:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:10px;">',
                obj.alternate_google_banner_ad.url
            )

        return "No Alternate Banner"

    alternate_banner_preview.short_description = "Current Alternate Banner"