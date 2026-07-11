# ==========================================
# MyCarMarket Australia
# Version: v2.0.3
# File: rentals/admin.py
# Description:
# Flexible rental administration with:
# - Car image previews
# - Coloured moderation status badges
# - Approval and rejection actions
# - Availability and active status badges
# - Maximum one rental image
# - Django 6 compatible HTML rendering
# ==========================================


# ==========================================
# SECTION 1 START
# Imports
# ==========================================

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from rentals.models import (
    RentalCar,
    RentalCarImage,
)

# ==========================================
# SECTION 1 END
# Imports
# ==========================================

# _____________________________________________


# ==========================================
# SECTION 2 START
# Rental Image Inline
# Maximum One Image Per Rental
# ==========================================

class RentalCarImageInline(admin.StackedInline):

    model = RentalCarImage

    extra = 0

    max_num = 1

    min_num = 0

    can_delete = True

    fields = [
        "image",
        "image_preview",
        "alt_text",
    ]

    readonly_fields = [
        "image_preview",
    ]

    verbose_name = (
        "Rental Car Photo"
    )

    verbose_name_plural = (
        "Rental Car Photo"
    )

    def image_preview(
        self,
        obj,
    ):

        if obj.pk and obj.image:

            return format_html(
                '<div style="margin-top: 10px;">'
                '<img src="{}" '
                'style="width: 100%; '
                'max-width: 520px; '
                'height: 300px; '
                'object-fit: cover; '
                'border-radius: 12px; '
                'border: 1px solid #d1d5db; '
                'box-shadow: 0 4px 14px '
                'rgba(0, 0, 0, 0.08);" '
                'alt="{}">'
                '</div>',
                obj.image.url,
                (
                    obj.alt_text
                    or "Rental car image"
                ),
            )

        return mark_safe(
            '<div style="padding: 18px; '
            'max-width: 480px; '
            'background: #f8fafc; '
            'border: 1px dashed #cbd5e1; '
            'border-radius: 10px; '
            'color: #64748b; '
            'text-align: center;">'
            'No car photo uploaded yet.'
            '</div>'
        )

    image_preview.short_description = (
        "Current Car Photo"
    )


# ==========================================
# SECTION 2 END
# Rental Image Inline
# ==========================================

# _____________________________________________


# ==========================================
# SECTION 3 START
# Rental Car Admin
# ==========================================

@admin.register(RentalCar)
class RentalCarAdmin(admin.ModelAdmin):

    list_display = [
        "rental_thumbnail",
        "title",
        "vehicle_display",
        "posted_by",
        "location_display",
        "daily_price_display",
        "moderation_status_badge",
        "availability_badge",
        "active_status_badge",
        "is_featured",
        "created_at",
    ]

    list_display_links = [
        "rental_thumbnail",
        "title",
    ]

    list_filter = [
        "moderation_status",
        "is_approved",
        "is_available",
        "is_active",
        "is_featured",
        "state",
        "body_type",
        "transmission",
        "fuel_type",
        "created_at",
    ]

    search_fields = [
        "title",
        "make",
        "model",
        "year",
        "suburb",
        "state",
        "postcode",
        "owner_name",
        "owner_email",
        "owner_phone",
        "registration_number",
        "posted_by__username",
        "posted_by__email",
        "posted_by__first_name",
        "posted_by__last_name",
    ]

    readonly_fields = [
        "slug",
        "main_image_preview",
        "moderation_status_preview",
        "views",
        "approved_at",
        "created_at",
        "updated_at",
    ]

    autocomplete_fields = [
        "posted_by",
    ]

    list_editable = [
        "is_featured",
    ]

    ordering = [
        "-is_featured",
        "-created_at",
    ]

    date_hierarchy = "created_at"

    list_per_page = 25

    save_on_top = True

    inlines = [
        RentalCarImageInline,
    ]

    actions = [
        "approve_selected_rentals",
        "reject_selected_rentals",
        "mark_as_pending",
        "mark_as_available",
        "mark_as_unavailable",
        "activate_selected_rentals",
        "deactivate_selected_rentals",
        "feature_selected_rentals",
        "remove_featured_status",
    ]

    fieldsets = [

        (
            "Rental Listing",
            {
                "fields": [
                    "posted_by",
                    "title",
                    "slug",
                    "main_image_preview",
                ],
            },
        ),

        (
            "Moderation Status",
            {
                "fields": [
                    "moderation_status_preview",
                    (
                        "moderation_status",
                        "is_approved",
                    ),
                    "rejection_reason",
                    "approved_at",
                ],
            },
        ),

        (
            "Vehicle Details",
            {
                "fields": [
                    (
                        "make",
                        "model",
                        "year",
                    ),
                    (
                        "body_type",
                        "transmission",
                        "fuel_type",
                    ),
                    (
                        "seats",
                        "colour",
                        "registration_number",
                    ),
                ],
            },
        ),

        (
            "Rental Pricing",
            {
                "fields": [
                    (
                        "daily_price",
                        "weekly_price",
                    ),
                    (
                        "security_deposit",
                        "minimum_rental_days",
                    ),
                    (
                        "unlimited_kilometres",
                        "daily_kilometre_limit",
                    ),
                ],
            },
        ),

        (
            "Rental Information",
            {
                "fields": [
                    "description",
                    "rental_conditions",
                ],
            },
        ),

        (
            "Pickup Location",
            {
                "fields": [
                    "pickup_address",
                    (
                        "suburb",
                        "state",
                        "postcode",
                    ),
                ],
            },
        ),

        (
            "Owner Contact Details",
            {
                "fields": [
                    "owner_name",
                    "owner_email",
                    "owner_phone",
                ],
            },
        ),

        (
            "Availability",
            {
                "fields": [
                    (
                        "available_from",
                        "available_until",
                    ),
                    "is_available",
                ],
            },
        ),

        (
            "Listing Controls",
            {
                "fields": [
                    (
                        "is_active",
                        "is_featured",
                    ),
                    "views",
                ],
            },
        ),

        (
            "System Information",
            {
                "classes": [
                    "collapse",
                ],
                "fields": [
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]

    def save_model(
        self,
        request,
        obj,
        form,
        change,
    ):

        if (
            obj.moderation_status
            == "approved"
        ):

            obj.is_approved = True

            obj.rejection_reason = ""

            if not obj.approved_at:

                obj.approved_at = (
                    timezone.now()
                )

        elif (
            obj.moderation_status
            == "rejected"
        ):

            obj.is_approved = False

            obj.approved_at = None

        else:

            obj.is_approved = False

            obj.approved_at = None

            obj.rejection_reason = ""

        super().save_model(
            request,
            obj,
            form,
            change,
        )

    def rental_thumbnail(
        self,
        obj,
    ):

        primary_image = (
            obj.primary_image
        )

        if (
            primary_image
            and primary_image.image
        ):

            return format_html(
                '<img src="{}" '
                'style="width: 90px; '
                'height: 60px; '
                'object-fit: cover; '
                'border-radius: 8px; '
                'border: 1px solid #d1d5db; '
                'box-shadow: 0 2px 6px '
                'rgba(0, 0, 0, 0.08);" '
                'alt="{}">',
                primary_image.image.url,
                (
                    primary_image.alt_text
                    or obj.title
                ),
            )

        return mark_safe(
            '<div style="width: 90px; '
            'height: 60px; '
            'display: flex; '
            'align-items: center; '
            'justify-content: center; '
            'background: #f1f5f9; '
            'border: 1px dashed #cbd5e1; '
            'border-radius: 8px; '
            'font-size: 11px; '
            'color: #64748b; '
            'text-align: center;">'
            'No photo'
            '</div>'
        )

    rental_thumbnail.short_description = (
        "Car Photo"
    )

    def main_image_preview(
        self,
        obj,
    ):

        if not obj.pk:

            return mark_safe(
                '<div style="padding: 16px; '
                'background: #f8fafc; '
                'border: 1px dashed #cbd5e1; '
                'border-radius: 10px; '
                'color: #64748b;">'
                'Save the rental listing first, '
                'then upload one car photo below.'
                '</div>'
            )

        primary_image = (
            obj.primary_image
        )

        if (
            primary_image
            and primary_image.image
        ):

            return format_html(
                '<div style="margin-top: 8px;">'
                '<img src="{}" '
                'style="width: 100%; '
                'max-width: 620px; '
                'height: 360px; '
                'object-fit: cover; '
                'border-radius: 14px; '
                'border: 1px solid #d1d5db; '
                'box-shadow: 0 5px 18px '
                'rgba(0, 0, 0, 0.10);" '
                'alt="{}">'
                '</div>',
                primary_image.image.url,
                (
                    primary_image.alt_text
                    or obj.title
                ),
            )

        return mark_safe(
            '<div style="padding: 20px; '
            'max-width: 580px; '
            'background: #fff7ed; '
            'border: 1px solid #fed7aa; '
            'border-radius: 10px; '
            'color: #9a3412;">'
            '<strong>No car photo uploaded.</strong>'
            '<br>'
            'Upload one image in the '
            'Rental Car Photo section below.'
            '</div>'
        )

    main_image_preview.short_description = (
        "Main Car Image"
    )

    def vehicle_display(
        self,
        obj,
    ):

        return (
            f"{obj.year} "
            f"{obj.make} "
            f"{obj.model}"
        )

    vehicle_display.short_description = (
        "Vehicle"
    )

    vehicle_display.admin_order_field = (
        "year"
    )

    def moderation_status_badge(
        self,
        obj,
    ):

        status_styles = {
            "approved": {
                "label": "Approved",
                "background": "#dcfce7",
                "colour": "#166534",
                "border": "#86efac",
            },
            "pending": {
                "label": "Pending",
                "background": "#fef3c7",
                "colour": "#92400e",
                "border": "#fcd34d",
            },
            "rejected": {
                "label": "Rejected",
                "background": "#fee2e2",
                "colour": "#991b1b",
                "border": "#fca5a5",
            },
        }

        style = status_styles.get(
            obj.moderation_status,
            {
                "label": (
                    obj.get_moderation_status_display()
                ),
                "background": "#f1f5f9",
                "colour": "#475569",
                "border": "#cbd5e1",
            },
        )

        return format_html(
            '<span style="display: inline-block; '
            'min-width: 76px; '
            'padding: 5px 10px; '
            'background: {}; '
            'color: {}; '
            'border: 1px solid {}; '
            'border-radius: 999px; '
            'font-size: 12px; '
            'font-weight: 700; '
            'text-align: center;">'
            '{}'
            '</span>',
            style["background"],
            style["colour"],
            style["border"],
            style["label"],
        )

    moderation_status_badge.short_description = (
        "Status"
    )

    moderation_status_badge.admin_order_field = (
        "moderation_status"
    )

    def moderation_status_preview(
        self,
        obj,
    ):

        if not obj.pk:

            return mark_safe(
                '<span style="display: inline-block; '
                'padding: 8px 15px; '
                'background: #fef3c7; '
                'color: #92400e; '
                'border: 1px solid #fcd34d; '
                'border-radius: 999px; '
                'font-weight: 700;">'
                'New Listing – Pending'
                '</span>'
            )

        return self.moderation_status_badge(
            obj
        )

    moderation_status_preview.short_description = (
        "Current Status"
    )

    def availability_badge(
        self,
        obj,
    ):

        if obj.is_available:

            return mark_safe(
                '<span style="display: inline-block; '
                'padding: 5px 10px; '
                'background: #dbeafe; '
                'color: #1e40af; '
                'border: 1px solid #93c5fd; '
                'border-radius: 999px; '
                'font-size: 12px; '
                'font-weight: 700;">'
                'Available'
                '</span>'
            )

        return mark_safe(
            '<span style="display: inline-block; '
            'padding: 5px 10px; '
            'background: #f1f5f9; '
            'color: #475569; '
            'border: 1px solid #cbd5e1; '
            'border-radius: 999px; '
            'font-size: 12px; '
            'font-weight: 700;">'
            'Unavailable'
            '</span>'
        )

    availability_badge.short_description = (
        "Availability"
    )

    availability_badge.admin_order_field = (
        "is_available"
    )

    def active_status_badge(
        self,
        obj,
    ):

        if obj.is_active:

            return mark_safe(
                '<span style="display: inline-block; '
                'padding: 5px 10px; '
                'background: #ecfdf5; '
                'color: #047857; '
                'border: 1px solid #a7f3d0; '
                'border-radius: 999px; '
                'font-size: 12px; '
                'font-weight: 700;">'
                'Active'
                '</span>'
            )

        return mark_safe(
            '<span style="display: inline-block; '
            'padding: 5px 10px; '
            'background: #f3f4f6; '
            'color: #6b7280; '
            'border: 1px solid #d1d5db; '
            'border-radius: 999px; '
            'font-size: 12px; '
            'font-weight: 700;">'
            'Inactive'
            '</span>'
        )

    active_status_badge.short_description = (
        "Listing"
    )

    active_status_badge.admin_order_field = (
        "is_active"
    )

    def location_display(
        self,
        obj,
    ):

        return obj.location

    location_display.short_description = (
        "Location"
    )

    location_display.admin_order_field = (
        "suburb"
    )

    def daily_price_display(
        self,
        obj,
    ):

        return (
            f"${obj.daily_price:,.2f} / day"
        )

    daily_price_display.short_description = (
        "Daily Price"
    )

    daily_price_display.admin_order_field = (
        "daily_price"
    )

    @admin.action(
        description=(
            "Approve selected rental listings"
        )
    )
    def approve_selected_rentals(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            moderation_status="approved",
            is_approved=True,
            rejection_reason="",
            approved_at=timezone.now(),
        )

        self.message_user(
            request,
            (
                f"{updated} rental listing"
                f"{'s' if updated != 1 else ''} "
                f"approved."
            ),
        )

    @admin.action(
        description=(
            "Reject selected rental listings"
        )
    )
    def reject_selected_rentals(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            moderation_status="rejected",
            is_approved=False,
            approved_at=None,
        )

        self.message_user(
            request,
            (
                f"{updated} rental listing"
                f"{'s' if updated != 1 else ''} "
                f"rejected."
            ),
        )

    @admin.action(
        description=(
            "Move selected rental listings "
            "to pending"
        )
    )
    def mark_as_pending(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            moderation_status="pending",
            is_approved=False,
            rejection_reason="",
            approved_at=None,
        )

        self.message_user(
            request,
            (
                f"{updated} rental listing"
                f"{'s' if updated != 1 else ''} "
                f"moved to pending."
            ),
        )

    @admin.action(
        description=(
            "Mark selected rentals as available"
        )
    )
    def mark_as_available(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            is_available=True,
        )

        self.message_user(
            request,
            (
                f"{updated} rental listing"
                f"{'s' if updated != 1 else ''} "
                f"marked as available."
            ),
        )

    @admin.action(
        description=(
            "Mark selected rentals as unavailable"
        )
    )
    def mark_as_unavailable(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            is_available=False,
        )

        self.message_user(
            request,
            (
                f"{updated} rental listing"
                f"{'s' if updated != 1 else ''} "
                f"marked as unavailable."
            ),
        )

    @admin.action(
        description=(
            "Activate selected rental listings"
        )
    )
    def activate_selected_rentals(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            (
                f"{updated} rental listing"
                f"{'s' if updated != 1 else ''} "
                f"activated."
            ),
        )

    @admin.action(
        description=(
            "Deactivate selected rental listings"
        )
    )
    def deactivate_selected_rentals(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            (
                f"{updated} rental listing"
                f"{'s' if updated != 1 else ''} "
                f"deactivated."
            ),
        )

    @admin.action(
        description=(
            "Feature selected rental listings"
        )
    )
    def feature_selected_rentals(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            is_featured=True,
        )

        self.message_user(
            request,
            (
                f"{updated} rental listing"
                f"{'s' if updated != 1 else ''} "
                f"featured."
            ),
        )

    @admin.action(
        description=(
            "Remove featured status"
        )
    )
    def remove_featured_status(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            is_featured=False,
        )

        self.message_user(
            request,
            (
                f"Featured status removed from "
                f"{updated} rental listing"
                f"{'s' if updated != 1 else ''}."
            ),
        )


# ==========================================
# SECTION 3 END
# Rental Car Admin
# ==========================================

# _____________________________________________


# ==========================================
# SECTION 4 START
# Rental Image Admin
# ==========================================

@admin.register(RentalCarImage)
class RentalCarImageAdmin(admin.ModelAdmin):

    list_display = [
        "image_thumbnail",
        "rental",
        "rental_status_badge",
        "created_at",
    ]

    list_display_links = [
        "image_thumbnail",
        "rental",
    ]

    list_filter = [
        "rental__moderation_status",
        "rental__is_available",
        "rental__is_active",
        "created_at",
    ]

    search_fields = [
        "rental__title",
        "rental__make",
        "rental__model",
        "rental__owner_name",
        "alt_text",
    ]

    autocomplete_fields = [
        "rental",
    ]

    readonly_fields = [
        "image_preview",
        "rental_status_preview",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]

    list_per_page = 25

    fields = [
        "rental",
        "rental_status_preview",
        "image",
        "image_preview",
        "alt_text",
        "created_at",
    ]

    def image_thumbnail(
        self,
        obj,
    ):

        if obj.image:

            return format_html(
                '<img src="{}" '
                'style="width: 90px; '
                'height: 60px; '
                'object-fit: cover; '
                'border-radius: 8px; '
                'border: 1px solid #d1d5db; '
                'box-shadow: 0 2px 6px '
                'rgba(0, 0, 0, 0.08);" '
                'alt="{}">',
                obj.image.url,
                (
                    obj.alt_text
                    or "Rental car image"
                ),
            )

        return mark_safe(
            '<div style="width: 90px; '
            'height: 60px; '
            'display: flex; '
            'align-items: center; '
            'justify-content: center; '
            'background: #f1f5f9; '
            'border: 1px dashed #cbd5e1; '
            'border-radius: 8px; '
            'font-size: 11px; '
            'color: #64748b;">'
            'No photo'
            '</div>'
        )

    image_thumbnail.short_description = (
        "Car Photo"
    )

    def image_preview(
        self,
        obj,
    ):

        if obj.image:

            return format_html(
                '<img src="{}" '
                'style="width: 100%; '
                'max-width: 620px; '
                'height: 360px; '
                'object-fit: cover; '
                'border-radius: 14px; '
                'border: 1px solid #d1d5db; '
                'box-shadow: 0 5px 18px '
                'rgba(0, 0, 0, 0.10);" '
                'alt="{}">',
                obj.image.url,
                (
                    obj.alt_text
                    or "Rental car image"
                ),
            )

        return mark_safe(
            '<div style="padding: 18px; '
            'background: #f8fafc; '
            'border: 1px dashed #cbd5e1; '
            'border-radius: 10px; '
            'color: #64748b;">'
            'No rental car image uploaded.'
            '</div>'
        )

    image_preview.short_description = (
        "Large Image Preview"
    )

    def rental_status_badge(
        self,
        obj,
    ):

        status = (
            obj.rental.moderation_status
        )

        if status == "approved":

            return mark_safe(
                '<span style="padding: 5px 10px; '
                'background: #dcfce7; '
                'color: #166534; '
                'border: 1px solid #86efac; '
                'border-radius: 999px; '
                'font-size: 12px; '
                'font-weight: 700;">'
                'Approved'
                '</span>'
            )

        if status == "rejected":

            return mark_safe(
                '<span style="padding: 5px 10px; '
                'background: #fee2e2; '
                'color: #991b1b; '
                'border: 1px solid #fca5a5; '
                'border-radius: 999px; '
                'font-size: 12px; '
                'font-weight: 700;">'
                'Rejected'
                '</span>'
            )

        return mark_safe(
            '<span style="padding: 5px 10px; '
            'background: #fef3c7; '
            'color: #92400e; '
            'border: 1px solid #fcd34d; '
            'border-radius: 999px; '
            'font-size: 12px; '
            'font-weight: 700;">'
            'Pending'
            '</span>'
        )

    rental_status_badge.short_description = (
        "Rental Status"
    )

    rental_status_badge.admin_order_field = (
        "rental__moderation_status"
    )

    def rental_status_preview(
        self,
        obj,
    ):

        if not obj.pk:

            return (
                "The rental status will appear "
                "after the image is saved."
            )

        return self.rental_status_badge(
            obj
        )

    rental_status_preview.short_description = (
        "Current Rental Status"
    )


# ==========================================
# SECTION 4 END
# Rental Image Admin
# ==========================================

# _____________________________________________