# ==========================================
# MyCarMarket
# Version: v1.12.3
# File: reviews/admin.py
# Description:
# Professional Car Review Admin
# Shows uploaded hero image or default review image
# ==========================================

from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html

from .models import CarReview


# ==========================================
# SECTION 01: CAR REVIEW ADMIN
# START
# ==========================================

@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):

    list_display = (
        "review_photo",
        "title",
        "make",
        "model",
        "year",
        "body_type",
        "rating",
        "published_status",
        "featured_status",
        "published_at",
    )

    list_display_links = (
        "review_photo",
        "title",
    )

    search_fields = (
        "title",
        "slug",
        "make",
        "model",
        "body_type",
        "meta_title",
        "meta_description",
    )

    list_filter = (
        "is_published",
        "is_featured",
        "body_type",
        "make",
        "published_at",
    )

    ordering = (
        "-is_featured",
        "-published_at",
    )

    list_per_page = 25

    readonly_fields = (
        "image_preview",
        "published_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Basic Review Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "make",
                    "model",
                    "year",
                    "body_type",
                    "rating",
                )
            },
        ),
        (
            "Review Image",
            {
                "fields": (
                    "image_preview",
                    "hero_image",
                )
            },
        ),
        (
            "Review Content",
            {
                "fields": (
                    "summary",
                    "pros",
                    "cons",
                    "content",
                    "faq",
                )
            },
        ),
        (
            "SEO Settings",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "is_published",
                    "is_featured",
                    "published_at",
                    "updated_at",
                )
            },
        ),
    )

    # ==========================================
    # ADMIN LIST PHOTO
    # ==========================================

    def review_photo(self, obj):

        if obj.hero_image:
            image_url = obj.hero_image.url
        else:
            image_url = static("images/default-review.png")

        return format_html(
            '<img src="{}" style="width:100px;height:65px;object-fit:cover;border-radius:8px;border:1px solid #ddd;" />',
            image_url,
        )

    review_photo.short_description = "Photo"

    # ==========================================
    # ADMIN EDIT PAGE IMAGE PREVIEW
    # ==========================================

    def image_preview(self, obj):

        if obj and obj.hero_image:
            image_url = obj.hero_image.url
        else:
            image_url = static("images/default-review.png")

        return format_html(
            '<img src="{}" style="width:320px;height:180px;object-fit:cover;border-radius:12px;border:1px solid #ddd;" />',
            image_url,
        )

    image_preview.short_description = "Current Image"

    # ==========================================
    # PUBLISHED STATUS
    # ==========================================

    def published_status(self, obj):

        if obj.is_published:
            return "✅ Published"

        return "❌ Draft"

    published_status.short_description = "Status"

    # ==========================================
    # FEATURED STATUS
    # ==========================================

    def featured_status(self, obj):

        if obj.is_featured:
            return "⭐ Featured"

        return "-"

    featured_status.short_description = "Featured"


# ==========================================
# SECTION 01: CAR REVIEW ADMIN
# END
# ==========================================