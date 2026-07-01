# ==========================================
# MyCarMarket
# Version: v1.5.3
# File: vehicles/admin/car_admin.py
# Description: Vehicle Moderation Center + Improved Car Admin Approval
# ==========================================

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from vehicles.models import Car
from .car_image_admin import CarImageInline


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'admin_thumbnail',
        'title',
        'posted_by',
        'make',
        'model',
        'year',
        'price',
        'state',
        'suburb',
        'moderation_status_badge',
        'report_badge',
        'is_approved',
        'is_active',
        'is_featured',
        'is_verified_listing',
        'views_count',
        'created_at',
    )

    list_editable = (
        'is_featured',
        'is_verified_listing',
    )

    list_filter = (
        'moderation_status',
        'is_reported',
        'is_approved',
        'is_active',
        'is_featured',
        'is_verified_listing',
        'state',
        'make',
        'body_type',
        'fuel_type',
        'transmission',
        'seller',
        'created_at',
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
        'rejected_reason',
        'admin_note',
        'suspended_reason',
    )

    readonly_fields = (
        'views_count',
        'created_at',
        'approved_at',
        'approved_by',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 25

    fieldsets = (
        (
            'Vehicle Details',
            {
                'fields': (
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
                )
            }
        ),
        (
            'Seller Details',
            {
                'fields': (
                    'seller',
                    'seller_name',
                    'seller_email',
                    'seller_phone',
                )
            }
        ),
        (
            'Moderation Center',
            {
                'fields': (
                    'moderation_status',
                    'is_approved',
                    'is_active',
                    'approved_by',
                    'approved_at',
                    'rejected_reason',
                    'suspended_reason',
                    'admin_note',
                    'is_reported',
                    'report_count',
                )
            }
        ),
        (
            'Promotion & Trust',
            {
                'fields': (
                    'is_featured',
                    'featured_until',
                    'is_verified_listing',
                )
            }
        ),
        (
            'Stats',
            {
                'fields': (
                    'views_count',
                    'created_at',
                )
            }
        ),
    )

    actions = (
        'approve_selected_listings',
        'reject_selected_listings',
        'suspend_selected_listings',
        'restore_to_pending',
        'activate_selected_listings',
        'deactivate_selected_listings',
        'mark_as_featured',
        'remove_featured',
        'mark_as_verified_listing',
        'remove_verified_listing',
        'mark_as_reported',
        'clear_reported_status',
    )

    inlines = [CarImageInline]

    def save_model(self, request, obj, form, change):

        if obj.moderation_status == 'approved':
            obj.is_approved = True
            obj.is_active = True

            if not obj.approved_by:
                obj.approved_by = request.user

            if not obj.approved_at:
                obj.approved_at = timezone.now()

        if obj.moderation_status == 'pending':
            obj.is_approved = False

        if obj.moderation_status == 'rejected':
            obj.is_approved = False
            obj.is_active = False

        if obj.moderation_status == 'suspended':
            obj.is_approved = False
            obj.is_active = False

        super().save_model(request, obj, form, change)

    def admin_thumbnail(self, obj):
        primary_image = obj.images.filter(
            is_primary=True
        ).first()

        if not primary_image:
            primary_image = obj.images.first()

        if primary_image and primary_image.image:
            return format_html(
                '<img src="{}" '
                'style="width:75px;height:55px;object-fit:cover;'
                'border-radius:8px;border:1px solid #ddd;" />',
                primary_image.image.url
            )

        return "No Image"

    admin_thumbnail.short_description = "Image"

    def moderation_status_badge(self, obj):

        if obj.moderation_status == 'approved':
            return mark_safe(
                '<span style="background:#dcfce7;color:#166534;'
                'padding:4px 10px;border-radius:999px;'
                'font-weight:700;font-size:12px;">'
                '✅ Approved'
                '</span>'
            )

        if obj.moderation_status == 'rejected':
            return mark_safe(
                '<span style="background:#fee2e2;color:#991b1b;'
                'padding:4px 10px;border-radius:999px;'
                'font-weight:700;font-size:12px;">'
                '❌ Rejected'
                '</span>'
            )

        if obj.moderation_status == 'suspended':
            return mark_safe(
                '<span style="background:#e5e7eb;color:#111827;'
                'padding:4px 10px;border-radius:999px;'
                'font-weight:700;font-size:12px;">'
                '🚫 Suspended'
                '</span>'
            )

        return mark_safe(
            '<span style="background:#fef3c7;color:#92400e;'
            'padding:4px 10px;border-radius:999px;'
            'font-weight:700;font-size:12px;">'
            '⏳ Pending'
            '</span>'
        )

    moderation_status_badge.short_description = "Moderation"

    def report_badge(self, obj):

        if obj.is_reported or obj.report_count > 0:
            return mark_safe(
                '<span style="background:#fee2e2;color:#991b1b;'
                'padding:4px 10px;border-radius:999px;'
                'font-weight:700;font-size:12px;">'
                f'🚨 {obj.report_count}'
                '</span>'
            )

        return mark_safe(
            '<span style="background:#dcfce7;color:#166534;'
            'padding:4px 10px;border-radius:999px;'
            'font-weight:700;font-size:12px;">'
            'Clear'
            '</span>'
        )

    report_badge.short_description = "Reports"

    def posted_by(self, obj):
        if obj.seller:
            return obj.seller.username

        if obj.seller_name:
            return obj.seller_name

        return "No User"

    posted_by.short_description = "Posted By"

    def approve_selected_listings(self, request, queryset):
        updated = queryset.update(
            moderation_status='approved',
            is_approved=True,
            is_active=True,
            approved_by=request.user,
            approved_at=timezone.now(),
        )

        self.message_user(
            request,
            f'{updated} listing(s) approved successfully.'
        )

    approve_selected_listings.short_description = "✅ Approve selected listings"

    def reject_selected_listings(self, request, queryset):
        updated = queryset.update(
            moderation_status='rejected',
            is_approved=False,
            is_active=False,
        )

        self.message_user(
            request,
            f'{updated} listing(s) rejected successfully.'
        )

    reject_selected_listings.short_description = "❌ Reject selected listings"

    def suspend_selected_listings(self, request, queryset):
        updated = queryset.update(
            moderation_status='suspended',
            is_approved=False,
            is_active=False,
        )

        self.message_user(
            request,
            f'{updated} listing(s) suspended successfully.'
        )

    suspend_selected_listings.short_description = "🚫 Suspend selected listings"

    def restore_to_pending(self, request, queryset):
        updated = queryset.update(
            moderation_status='pending',
            is_approved=False,
            is_active=True,
            approved_by=None,
            approved_at=None,
        )

        self.message_user(
            request,
            f'{updated} listing(s) moved back to pending review.'
        )

    restore_to_pending.short_description = "⏳ Move selected listings to pending"

    def activate_selected_listings(self, request, queryset):
        updated = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            f'{updated} listing(s) activated successfully.'
        )

    activate_selected_listings.short_description = "Activate selected listings"

    def deactivate_selected_listings(self, request, queryset):
        updated = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            f'{updated} listing(s) deactivated successfully.'
        )

    deactivate_selected_listings.short_description = "Deactivate selected listings"

    def mark_as_featured(self, request, queryset):
        updated = queryset.update(
            is_featured=True,
        )

        self.message_user(
            request,
            f'{updated} listing(s) marked as featured.'
        )

    mark_as_featured.short_description = "⭐ Mark selected listings as featured"

    def remove_featured(self, request, queryset):
        updated = queryset.update(
            is_featured=False,
        )

        self.message_user(
            request,
            f'{updated} listing(s) removed from featured.'
        )

    remove_featured.short_description = "Remove selected listings from featured"

    def mark_as_verified_listing(self, request, queryset):
        updated = queryset.update(
            is_verified_listing=True,
        )

        self.message_user(
            request,
            f'{updated} listing(s) marked as verified.'
        )

    mark_as_verified_listing.short_description = "✔ Mark selected listings as verified"

    def remove_verified_listing(self, request, queryset):
        updated = queryset.update(
            is_verified_listing=False,
        )

        self.message_user(
            request,
            f'{updated} listing(s) removed from verified.'
        )

    remove_verified_listing.short_description = "Remove selected listings from verified"

    def mark_as_reported(self, request, queryset):
        updated = queryset.update(
            is_reported=True,
        )

        self.message_user(
            request,
            f'{updated} listing(s) marked as reported.'
        )

    mark_as_reported.short_description = "🚨 Mark selected listings as reported"

    def clear_reported_status(self, request, queryset):
        updated = queryset.update(
            is_reported=False,
            report_count=0,
        )

        self.message_user(
            request,
            f'{updated} listing report status cleared.'
        )

    clear_reported_status.short_description = "Clear reported status"