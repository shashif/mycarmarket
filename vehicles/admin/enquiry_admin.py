# ==========================================
# MyCarMarket
# Version: v0.9.4
# File: vehicles/admin/enquiry_admin.py
# Enquiry Admin
# ==========================================

from django.contrib import admin

from vehicles.models import Enquiry


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