# ==========================================
# MyCarMarket
# Version: v1.0.2
# File: core/admin.py
# Site Settings Admin Preview + Ad Type Switch
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
                    'google_adsense_code',
                )
            }
        ),
    )

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