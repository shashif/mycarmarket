# ==========================================
# MyCarMarket Australia
# Version: v2.2.4
# File: services/admin.py
# Location: services/admin.py
# Description:
# Car Services administration with:
# - Service image previews
# - Moderation status badges
# - Approval and rejection actions
# - Pending confirmation handled by services/views.py
# - Automatic approval confirmation email
# - Bulk approval email notifications
# - Duplicate approval email prevention
# - Active and featured controls
# - Maximum one service image
# - Service enquiry management
# Last Updated: 17 Jul 2026
# ==========================================


# ==========================================
# SECTION 1 START
# Imports
# ==========================================

from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from services.models import (
    CarService,
    CarServiceImage,
    ServiceEnquiry,
)

# ==========================================
# SECTION 1 END
# Imports
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 2 START
# Approval Email Helper
# ==========================================

def send_service_approval_email(
    service,
):

    sender_email = getattr(
        settings,
        "DEFAULT_FROM_EMAIL",
        "",
    )

    provider_email = (
        service.provider_email
        or ""
    ).strip()

    if not sender_email or not provider_email:

        return False

    try:

        service_path = reverse(
            "service_detail",
            kwargs={
                "slug": service.slug,
            },
        )

    except Exception:

        service_path = (
            service.get_absolute_url()
        )

    site_url = getattr(
        settings,
        "SITE_URL",
        "",
    ).rstrip("/")

    if site_url:

        service_url = (
            f"{site_url}{service_path}"
        )

    else:

        service_url = service_path

    subject = (
        "Your service listing has been approved"
    )

    message = (
        f"Hello {service.provider_name},\n\n"
        f"Good news! Your service listing has been "
        f"approved on MyCarMarket Australia.\n\n"
        f"Listing: {service.title}\n"
        f"Business: {service.business_name}\n"
        f"Category: {service.get_category_display()}\n"
        f"Location: {service.location}\n\n"
        f"Your listing is now publicly available at:\n"
        f"{service_url}\n\n"
        f"Customers can now view your listing and send "
        f"enquiries through MyCarMarket Australia.\n\n"
        f"Regards,\n"
        f"MyCarMarket Australia"
    )

    try:

        sent_count = send_mail(
            subject=subject,
            message=message,
            from_email=sender_email,
            recipient_list=[
                provider_email,
            ],
            fail_silently=False,
        )

        return sent_count > 0

    except Exception:

        return False


# ==========================================
# SECTION 2 END
# Approval Email Helper
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 3 START
# Service Image Inline
# Maximum One Image Per Service
# ==========================================

class CarServiceImageInline(admin.StackedInline):

    model = CarServiceImage

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

    verbose_name = "Service Image"

    verbose_name_plural = "Service Image"

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
                    or "Service image"
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
            'No service image uploaded yet.'
            '</div>'
        )

    image_preview.short_description = (
        "Current Service Image"
    )


# ==========================================
# SECTION 3 END
# Service Image Inline
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 4 START
# Car Service Admin
# ==========================================

@admin.register(CarService)
class CarServiceAdmin(admin.ModelAdmin):

    list_display = [
        "service_thumbnail",
        "title",
        "business_name",
        "category_display",
        "posted_by",
        "location_display",
        "price_display",
        "mobile_service_badge",
        "moderation_status_badge",
        "active_status_badge",
        "is_featured",
        "created_at",
    ]

    list_display_links = [
        "service_thumbnail",
        "title",
    ]

    list_filter = [
        "moderation_status",
        "is_approved",
        "is_active",
        "is_featured",
        "mobile_service",
        "category",
        "state",
        "created_at",
    ]

    search_fields = [
        "title",
        "business_name",
        "description",
        "suburb",
        "state",
        "postcode",
        "service_area",
        "provider_name",
        "provider_email",
        "provider_phone",
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
        CarServiceImageInline,
    ]

    actions = [
        "approve_selected_services",
        "reject_selected_services",
        "mark_as_pending",
        "activate_selected_services",
        "deactivate_selected_services",
        "feature_selected_services",
        "remove_featured_status",
        "mark_as_mobile_service",
        "remove_mobile_service_status",
    ]

    fieldsets = [

        (
            "Service Listing",
            {
                "fields": [
                    "posted_by",
                    "title",
                    "slug",
                    "business_name",
                    "category",
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
            "Service Information",
            {
                "fields": [
                    "description",
                    "mobile_service",
                    "starting_price",
                    "website",
                ],
            },
        ),

        (
            "Service Location",
            {
                "fields": [
                    (
                        "suburb",
                        "state",
                        "postcode",
                    ),
                    "service_area",
                ],
            },
        ),

        (
            "Provider Contact Details",
            {
                "fields": [
                    "provider_name",
                    "provider_email",
                    "provider_phone",
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

        was_approved = False

        if change and obj.pk:

            previous_service = (
                CarService.objects
                .filter(
                    pk=obj.pk,
                )
                .only(
                    "moderation_status",
                    "is_approved",
                )
                .first()
            )

            if previous_service:

                was_approved = (
                    previous_service.moderation_status
                    == "approved"
                    and previous_service.is_approved
                )

        if obj.moderation_status == "approved":

            obj.is_approved = True

            obj.rejection_reason = ""

            if not obj.approved_at:

                obj.approved_at = timezone.now()

        elif obj.moderation_status == "rejected":

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

        is_now_approved = (
            obj.moderation_status == "approved"
            and obj.is_approved
        )

        if is_now_approved and not was_approved:

            email_sent = (
                send_service_approval_email(
                    obj
                )
            )

            if email_sent:

                self.message_user(
                    request,
                    (
                        "The service listing was approved "
                        "and the provider confirmation email "
                        "was sent successfully."
                    ),
                    level="success",
                )

            else:

                self.message_user(
                    request,
                    (
                        "The service listing was approved, "
                        "but the provider confirmation email "
                        "could not be sent. Check the email "
                        "settings and provider email address."
                    ),
                    level="warning",
                )

    def service_thumbnail(
        self,
        obj,
    ):

        primary_image = obj.primary_image

        if primary_image and primary_image.image:

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
            'No image'
            '</div>'
        )

    service_thumbnail.short_description = (
        "Service Image"
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
                'Save the service listing first, '
                'then upload one service image below.'
                '</div>'
            )

        primary_image = obj.primary_image

        if primary_image and primary_image.image:

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
            '<strong>No service image uploaded.</strong>'
            '<br>'
            'Upload one image in the '
            'Service Image section below.'
            '</div>'
        )

    main_image_preview.short_description = (
        "Main Service Image"
    )

    def category_display(
        self,
        obj,
    ):

        return obj.get_category_display()

    category_display.short_description = (
        "Category"
    )

    category_display.admin_order_field = (
        "category"
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

    def price_display(
        self,
        obj,
    ):

        return obj.display_price

    price_display.short_description = (
        "Starting Price"
    )

    price_display.admin_order_field = (
        "starting_price"
    )

    def mobile_service_badge(
        self,
        obj,
    ):

        if obj.mobile_service:

            return mark_safe(
                '<span style="display: inline-block; '
                'padding: 5px 10px; '
                'background: #dbeafe; '
                'color: #1e40af; '
                'border: 1px solid #93c5fd; '
                'border-radius: 999px; '
                'font-size: 12px; '
                'font-weight: 700;">'
                'Mobile'
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
            'Fixed Location'
            '</span>'
        )

    mobile_service_badge.short_description = (
        "Service Type"
    )

    mobile_service_badge.admin_order_field = (
        "mobile_service"
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

    @admin.action(
        description="Approve selected service listings"
    )
    def approve_selected_services(
        self,
        request,
        queryset,
    ):

        services_to_approve = list(
            queryset.exclude(
                moderation_status="approved",
                is_approved=True,
            )
        )

        approved_count = 0

        email_sent_count = 0

        email_failed_count = 0

        for service in services_to_approve:

            service.moderation_status = (
                "approved"
            )

            service.is_approved = True

            service.rejection_reason = ""

            if not service.approved_at:

                service.approved_at = (
                    timezone.now()
                )

            service.save(
                update_fields=[
                    "moderation_status",
                    "is_approved",
                    "rejection_reason",
                    "approved_at",
                    "updated_at",
                ],
            )

            approved_count += 1

            if send_service_approval_email(
                service
            ):

                email_sent_count += 1

            else:

                email_failed_count += 1

        already_approved_count = (
            queryset.count()
            - approved_count
        )

        message_parts = [
            (
                f"{approved_count} service listing"
                f"{'s' if approved_count != 1 else ''} "
                f"approved"
            ),
            (
                f"{email_sent_count} approval email"
                f"{'s' if email_sent_count != 1 else ''} "
                f"sent"
            ),
        ]

        if already_approved_count:

            message_parts.append(
                (
                    f"{already_approved_count} already "
                    f"approved and skipped"
                )
            )

        if email_failed_count:

            message_parts.append(
                (
                    f"{email_failed_count} email"
                    f"{'s' if email_failed_count != 1 else ''} "
                    f"failed"
                )
            )

        self.message_user(
            request,
            "; ".join(message_parts) + ".",
            level=(
                "warning"
                if email_failed_count
                else "success"
            ),
        )

    @admin.action(
        description="Reject selected service listings"
    )
    def reject_selected_services(
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
                f"{updated} service listing"
                f"{'s' if updated != 1 else ''} "
                f"rejected."
            ),
        )

    @admin.action(
        description="Move selected service listings to pending"
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
                f"{updated} service listing"
                f"{'s' if updated != 1 else ''} "
                f"moved to pending."
            ),
        )

    @admin.action(
        description="Activate selected service listings"
    )
    def activate_selected_services(
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
                f"{updated} service listing"
                f"{'s' if updated != 1 else ''} "
                f"activated."
            ),
        )

    @admin.action(
        description="Deactivate selected service listings"
    )
    def deactivate_selected_services(
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
                f"{updated} service listing"
                f"{'s' if updated != 1 else ''} "
                f"deactivated."
            ),
        )

    @admin.action(
        description="Feature selected service listings"
    )
    def feature_selected_services(
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
                f"{updated} service listing"
                f"{'s' if updated != 1 else ''} "
                f"featured."
            ),
        )

    @admin.action(
        description="Remove featured status"
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
                f"{updated} service listing"
                f"{'s' if updated != 1 else ''}."
            ),
        )

    @admin.action(
        description="Mark selected listings as mobile services"
    )
    def mark_as_mobile_service(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            mobile_service=True,
        )

        self.message_user(
            request,
            (
                f"{updated} service listing"
                f"{'s' if updated != 1 else ''} "
                f"marked as mobile."
            ),
        )

    @admin.action(
        description="Remove mobile service status"
    )
    def remove_mobile_service_status(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            mobile_service=False,
        )

        self.message_user(
            request,
            (
                f"Mobile status removed from "
                f"{updated} service listing"
                f"{'s' if updated != 1 else ''}."
            ),
        )


# ==========================================
# SECTION 4 END
# Car Service Admin
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 5 START
# Service Image Admin
# ==========================================

@admin.register(CarServiceImage)
class CarServiceImageAdmin(admin.ModelAdmin):

    list_display = [
        "image_thumbnail",
        "service",
        "service_status_badge",
        "created_at",
    ]

    list_display_links = [
        "image_thumbnail",
        "service",
    ]

    list_filter = [
        "service__moderation_status",
        "service__is_active",
        "service__category",
        "created_at",
    ]

    search_fields = [
        "service__title",
        "service__business_name",
        "service__provider_name",
        "alt_text",
    ]

    autocomplete_fields = [
        "service",
    ]

    readonly_fields = [
        "image_preview",
        "service_status_preview",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]

    list_per_page = 25

    fields = [
        "service",
        "service_status_preview",
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
                    or "Service image"
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
            'No image'
            '</div>'
        )

    image_thumbnail.short_description = (
        "Service Image"
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
                    or "Service image"
                ),
            )

        return mark_safe(
            '<div style="padding: 18px; '
            'background: #f8fafc; '
            'border: 1px dashed #cbd5e1; '
            'border-radius: 10px; '
            'color: #64748b;">'
            'No service image uploaded.'
            '</div>'
        )

    image_preview.short_description = (
        "Large Image Preview"
    )

    def service_status_badge(
        self,
        obj,
    ):

        status = obj.service.moderation_status

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

    service_status_badge.short_description = (
        "Service Status"
    )

    service_status_badge.admin_order_field = (
        "service__moderation_status"
    )

    def service_status_preview(
        self,
        obj,
    ):

        if not obj.pk:

            return (
                "The service status will appear "
                "after the image is saved."
            )

        return self.service_status_badge(
            obj
        )

    service_status_preview.short_description = (
        "Current Service Status"
    )


# ==========================================
# SECTION 5 END
# Service Image Admin
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 6 START
# Service Enquiry Admin
# ==========================================

@admin.register(ServiceEnquiry)
class ServiceEnquiryAdmin(admin.ModelAdmin):

    list_display = [
        "customer_name",
        "service",
        "customer_email",
        "customer_phone",
        "status_badge",
        "provider_notified_badge",
        "created_at",
    ]

    list_display_links = [
        "customer_name",
        "service",
    ]

    list_filter = [
        "status",
        "provider_notified",
        "created_at",
        "service__category",
        "service__state",
    ]

    search_fields = [
        "customer_name",
        "customer_email",
        "customer_phone",
        "message",
        "service__title",
        "service__business_name",
        "service__provider_name",
        "service__provider_email",
    ]

    readonly_fields = [
        "customer_ip_address",
        "user_agent",
        "created_at",
        "updated_at",
    ]

    autocomplete_fields = [
        "service",
    ]

    ordering = [
        "-created_at",
    ]

    date_hierarchy = "created_at"

    list_per_page = 30

    save_on_top = True

    actions = [
        "mark_as_new",
        "mark_as_contacted",
        "mark_as_closed",
        "mark_as_spam",
        "mark_provider_notified",
        "mark_provider_not_notified",
    ]

    fieldsets = [

        (
            "Service Enquiry",
            {
                "fields": [
                    "service",
                    "status",
                    "provider_notified",
                ],
            },
        ),

        (
            "Customer Details",
            {
                "fields": [
                    "customer_name",
                    "customer_email",
                    "customer_phone",
                ],
            },
        ),

        (
            "Message",
            {
                "fields": [
                    "message",
                ],
            },
        ),

        (
            "Security Information",
            {
                "classes": [
                    "collapse",
                ],
                "fields": [
                    "customer_ip_address",
                    "user_agent",
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

    def status_badge(
        self,
        obj,
    ):

        status_styles = {
            "new": {
                "label": "New",
                "background": "#dbeafe",
                "colour": "#1e40af",
                "border": "#93c5fd",
            },
            "contacted": {
                "label": "Contacted",
                "background": "#fef3c7",
                "colour": "#92400e",
                "border": "#fcd34d",
            },
            "closed": {
                "label": "Closed",
                "background": "#dcfce7",
                "colour": "#166534",
                "border": "#86efac",
            },
            "spam": {
                "label": "Spam",
                "background": "#fee2e2",
                "colour": "#991b1b",
                "border": "#fca5a5",
            },
        }

        style = status_styles.get(
            obj.status,
            {
                "label": obj.get_status_display(),
                "background": "#f1f5f9",
                "colour": "#475569",
                "border": "#cbd5e1",
            },
        )

        return format_html(
            '<span style="display: inline-block; '
            'padding: 5px 10px; '
            'background: {}; '
            'color: {}; '
            'border: 1px solid {}; '
            'border-radius: 999px; '
            'font-size: 12px; '
            'font-weight: 700;">'
            '{}'
            '</span>',
            style["background"],
            style["colour"],
            style["border"],
            style["label"],
        )

    status_badge.short_description = (
        "Status"
    )

    status_badge.admin_order_field = (
        "status"
    )

    def provider_notified_badge(
        self,
        obj,
    ):

        if obj.provider_notified:

            return mark_safe(
                '<span style="padding: 5px 10px; '
                'background: #dcfce7; '
                'color: #166534; '
                'border: 1px solid #86efac; '
                'border-radius: 999px; '
                'font-size: 12px; '
                'font-weight: 700;">'
                'Notified'
                '</span>'
            )

        return mark_safe(
            '<span style="padding: 5px 10px; '
            'background: #f3f4f6; '
            'color: #6b7280; '
            'border: 1px solid #d1d5db; '
            'border-radius: 999px; '
            'font-size: 12px; '
            'font-weight: 700;">'
            'Not Sent'
            '</span>'
        )

    provider_notified_badge.short_description = (
        "Provider Email"
    )

    provider_notified_badge.admin_order_field = (
        "provider_notified"
    )

    @admin.action(
        description="Mark selected enquiries as new"
    )
    def mark_as_new(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            status="new",
        )

        self.message_user(
            request,
            f"{updated} enquiry record(s) marked as new.",
        )

    @admin.action(
        description="Mark selected enquiries as contacted"
    )
    def mark_as_contacted(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            status="contacted",
        )

        self.message_user(
            request,
            f"{updated} enquiry record(s) marked as contacted.",
        )

    @admin.action(
        description="Mark selected enquiries as closed"
    )
    def mark_as_closed(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            status="closed",
        )

        self.message_user(
            request,
            f"{updated} enquiry record(s) marked as closed.",
        )

    @admin.action(
        description="Mark selected enquiries as spam"
    )
    def mark_as_spam(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            status="spam",
        )

        self.message_user(
            request,
            f"{updated} enquiry record(s) marked as spam.",
        )

    @admin.action(
        description="Mark provider as notified"
    )
    def mark_provider_notified(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            provider_notified=True,
        )

        self.message_user(
            request,
            f"{updated} enquiry record(s) marked as notified.",
        )

    @admin.action(
        description="Mark provider as not notified"
    )
    def mark_provider_not_notified(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            provider_notified=False,
        )

        self.message_user(
            request,
            f"{updated} enquiry record(s) marked as not notified.",
        )


# ==========================================
# SECTION 6 END
# Service Enquiry Admin
# ==========================================
