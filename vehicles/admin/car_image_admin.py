# ==========================================
# MyCarMarket
# Version: v0.9.4
# File: vehicles/admin/car_image_admin.py
# Car Image Admin + Inline
# ==========================================

from django.contrib import admin
from django.utils.html import format_html

from vehicles.models import CarImage


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