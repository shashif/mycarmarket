# ==========================================
# MyCarMarket
# Version: v1.10.0
# File: vehicles/admin/pending_listing_admin.py
# Description:
# Admin Moderation Dashboard + Complete Listing Email Notifications
#
# Sends email when:
# 1. Admin approves listing
# 2. Admin rejects listing
# 3. Admin suspends listing
# Works for quick actions and bulk actions
# ==========================================

from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

from vehicles.models import Car
from vehicles.utils.email_notifications import (
    send_listing_approved_email,
    send_listing_rejected_email,
    send_listing_suspended_email,
)


# ==========================================
# SECTION 01 START
# Proxy Models
# ==========================================

class ModerationDashboard(Car):
    class Meta:
        proxy = True
        verbose_name = "Admin Dashboard"
        verbose_name_plural = "★ Admin Dashboard"


class PendingListing(Car):
    class Meta:
        proxy = True
        verbose_name = "Pending Listing"
        verbose_name_plural = "★ Pending Listings"


class ApprovedListing(Car):
    class Meta:
        proxy = True
        verbose_name = "Approved Listing"
        verbose_name_plural = "✅ Approved Listings"


class RejectedListing(Car):
    class Meta:
        proxy = True
        verbose_name = "Rejected Listing"
        verbose_name_plural = "❌ Rejected Listings"


class SuspendedListing(Car):
    class Meta:
        proxy = True
        verbose_name = "Suspended Listing"
        verbose_name_plural = "🚫 Suspended Listings"


class ReportedListing(Car):
    class Meta:
        proxy = True
        verbose_name = "Reported Listing"
        verbose_name_plural = "⚠️ Reported Listings"

# ==========================================
# SECTION 01 END
# ==========================================


# ==========================================
# SECTION 02 START
# Moderation Dashboard Admin
# ==========================================

@admin.register(ModerationDashboard)
class ModerationDashboardAdmin(admin.ModelAdmin):

    change_list_template = "admin/vehicles/moderation_dashboard.html"

    def changelist_view(self, request, extra_context=None):

        pending_listings = Car.objects.filter(
            moderation_status="pending"
        ).order_by("-created_at")[:10]

        reported_listings = Car.objects.filter(
            is_reported=True
        ).order_by("-report_count", "-created_at")[:10]

        extra_context = extra_context or {}

        extra_context.update({
            "pending_count": Car.objects.filter(moderation_status="pending").count(),
            "approved_count": Car.objects.filter(moderation_status="approved").count(),
            "rejected_count": Car.objects.filter(moderation_status="rejected").count(),
            "suspended_count": Car.objects.filter(moderation_status="suspended").count(),
            "reported_count": Car.objects.filter(is_reported=True).count(),
            "active_count": Car.objects.filter(is_active=True).count(),
            "featured_count": Car.objects.filter(is_featured=True).count(),
            "verified_count": Car.objects.filter(is_verified_listing=True).count(),
            "pending_listings": pending_listings,
            "reported_listings": reported_listings,
        })

        return super().changelist_view(
            request,
            extra_context=extra_context
        )

    def has_add_permission(self, request):
        return False

# ==========================================
# SECTION 02 END
# ==========================================


# ==========================================
# SECTION 03 START
# Base Moderation Admin
# ==========================================

class BaseModerationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "make",
        "model",
        "year",
        "price",
        "seller",
        "status_badge",
        "is_active",
        "report_count",
        "created_at",
        "quick_actions",
    )

    list_filter = (
        "make",
        "year",
        "state",
        "moderation_status",
        "is_active",
        "is_reported",
        "created_at",
    )

    search_fields = (
        "title",
        "make",
        "model",
        "seller__username",
        "seller__email",
        "seller_name",
        "seller_email",
        "seller_phone",
    )

    readonly_fields = (
        "created_at",
        "approved_by",
        "approved_at",
    )

    actions = (
        "approve_selected_listings",
        "reject_selected_listings",
        "suspend_selected_listings",
        "feature_selected_listings",
        "verify_selected_listings",
    )

    # ==========================================
    # SECTION 04 START
    # Status Badge
    # ==========================================

    def status_badge(self, obj):

        if obj.moderation_status == "approved":
            return format_html("<b style='color:green;'>✅ Approved</b>")

        if obj.moderation_status == "rejected":
            return format_html("<b style='color:red;'>❌ Rejected</b>")

        if obj.moderation_status == "suspended":
            return format_html("<b style='color:#555;'>🚫 Suspended</b>")

        return format_html("<b style='color:#d97706;'>⏳ Pending</b>")

    status_badge.short_description = "Status"

    # ==========================================
    # SECTION 04 END
    # ==========================================


    # ==========================================
    # SECTION 05 START
    # Quick Action Buttons
    # ==========================================

    def quick_actions(self, obj):

        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name

        approve_url = reverse(
            f"admin:{app_label}_{model_name}_quick_approve",
            args=[obj.id]
        )

        reject_url = reverse(
            f"admin:{app_label}_{model_name}_quick_reject",
            args=[obj.id]
        )

        suspend_url = reverse(
            f"admin:{app_label}_{model_name}_quick_suspend",
            args=[obj.id]
        )

        return format_html(
            """
            <a class="button" style="background:#16a34a;color:white;padding:5px 8px;border-radius:6px;" href="{}">Approve</a>
            <a class="button" style="background:#dc2626;color:white;padding:5px 8px;border-radius:6px;" href="{}">Reject</a>
            <a class="button" style="background:#374151;color:white;padding:5px 8px;border-radius:6px;" href="{}">Suspend</a>
            """,
            approve_url,
            reject_url,
            suspend_url,
        )

    quick_actions.short_description = "Quick Actions"

    # ==========================================
    # SECTION 05 END
    # ==========================================


    # ==========================================
    # SECTION 06 START
    # Custom Admin URLs
    # ==========================================

    def get_urls(self):

        urls = super().get_urls()

        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name

        custom_urls = [
            path(
                "<int:car_id>/quick-approve/",
                self.admin_site.admin_view(self.quick_approve),
                name=f"{app_label}_{model_name}_quick_approve",
            ),
            path(
                "<int:car_id>/quick-reject/",
                self.admin_site.admin_view(self.quick_reject),
                name=f"{app_label}_{model_name}_quick_reject",
            ),
            path(
                "<int:car_id>/quick-suspend/",
                self.admin_site.admin_view(self.quick_suspend),
                name=f"{app_label}_{model_name}_quick_suspend",
            ),
        ]

        return custom_urls + urls

    # ==========================================
    # SECTION 06 END
    # ==========================================


    # ==========================================
    # SECTION 07 START
    # Quick Action Methods
    # ==========================================

    def quick_approve(self, request, car_id):

        car = Car.objects.get(id=car_id)
        old_status = car.moderation_status

        car.moderation_status = "approved"
        car.is_approved = True
        car.is_active = True
        car.approved_by = request.user
        car.approved_at = timezone.now()
        car.save()

        if old_status != "approved":
            send_listing_approved_email(car)

        messages.success(
            request,
            f"{car.title} approved successfully. Approval email sent."
        )

        return redirect(
            request.META.get("HTTP_REFERER", "../")
        )

    def quick_reject(self, request, car_id):

        car = Car.objects.get(id=car_id)
        old_status = car.moderation_status

        car.moderation_status = "rejected"
        car.is_approved = False
        car.is_active = False
        car.save()

        if old_status != "rejected":
            send_listing_rejected_email(car)

        messages.warning(
            request,
            f"{car.title} rejected successfully. Rejection email sent."
        )

        return redirect(
            request.META.get("HTTP_REFERER", "../")
        )

    def quick_suspend(self, request, car_id):

        car = Car.objects.get(id=car_id)
        old_status = car.moderation_status

        car.moderation_status = "suspended"
        car.is_approved = False
        car.is_active = False
        car.save()

        if old_status != "suspended":
            send_listing_suspended_email(car)

        messages.warning(
            request,
            f"{car.title} suspended successfully. Suspension email sent."
        )

        return redirect(
            request.META.get("HTTP_REFERER", "../")
        )

    # ==========================================
    # SECTION 07 END
    # ==========================================


    # ==========================================
    # SECTION 08 START
    # Bulk Admin Actions
    # ==========================================

    @admin.action(description="Approve selected listings")
    def approve_selected_listings(self, request, queryset):

        updated = 0

        for car in queryset:
            old_status = car.moderation_status

            car.moderation_status = "approved"
            car.is_approved = True
            car.is_active = True
            car.approved_by = request.user
            car.approved_at = timezone.now()
            car.save()

            if old_status != "approved":
                send_listing_approved_email(car)

            updated += 1

        self.message_user(
            request,
            f"{updated} listing(s) approved successfully. Approval email(s) sent."
        )

    @admin.action(description="Reject selected listings")
    def reject_selected_listings(self, request, queryset):

        updated = 0

        for car in queryset:
            old_status = car.moderation_status

            car.moderation_status = "rejected"
            car.is_approved = False
            car.is_active = False
            car.save()

            if old_status != "rejected":
                send_listing_rejected_email(car)

            updated += 1

        self.message_user(
            request,
            f"{updated} listing(s) rejected successfully. Rejection email(s) sent."
        )

    @admin.action(description="Suspend selected listings")
    def suspend_selected_listings(self, request, queryset):

        updated = 0

        for car in queryset:
            old_status = car.moderation_status

            car.moderation_status = "suspended"
            car.is_approved = False
            car.is_active = False
            car.save()

            if old_status != "suspended":
                send_listing_suspended_email(car)

            updated += 1

        self.message_user(
            request,
            f"{updated} listing(s) suspended successfully. Suspension email(s) sent."
        )

    @admin.action(description="Make selected listings featured")
    def feature_selected_listings(self, request, queryset):

        updated = queryset.update(
            is_featured=True
        )

        self.message_user(
            request,
            f"{updated} listing(s) marked as featured."
        )

    @admin.action(description="Verify selected listings")
    def verify_selected_listings(self, request, queryset):

        updated = queryset.update(
            is_verified_listing=True
        )

        self.message_user(
            request,
            f"{updated} listing(s) verified successfully."
        )

    # ==========================================
    # SECTION 08 END
    # ==========================================


# ==========================================
# SECTION 09 START
# Pending Listings Admin
# ==========================================

@admin.register(PendingListing)
class PendingListingAdmin(BaseModerationAdmin):

    def get_queryset(self, request):

        return super().get_queryset(request).filter(
            moderation_status="pending"
        )

# ==========================================
# SECTION 09 END
# ==========================================


# ==========================================
# SECTION 10 START
# Approved Listings Admin
# ==========================================

@admin.register(ApprovedListing)
class ApprovedListingAdmin(BaseModerationAdmin):

    def get_queryset(self, request):

        return super().get_queryset(request).filter(
            moderation_status="approved"
        )

# ==========================================
# SECTION 10 END
# ==========================================


# ==========================================
# SECTION 11 START
# Rejected Listings Admin
# ==========================================

@admin.register(RejectedListing)
class RejectedListingAdmin(BaseModerationAdmin):

    def get_queryset(self, request):

        return super().get_queryset(request).filter(
            moderation_status="rejected"
        )

# ==========================================
# SECTION 11 END
# ==========================================


# ==========================================
# SECTION 12 START
# Suspended Listings Admin
# ==========================================

@admin.register(SuspendedListing)
class SuspendedListingAdmin(BaseModerationAdmin):

    def get_queryset(self, request):

        return super().get_queryset(request).filter(
            moderation_status="suspended"
        )

# ==========================================
# SECTION 12 END
# ==========================================


# ==========================================
# SECTION 13 START
# Reported Listings Admin
# ==========================================

@admin.register(ReportedListing)
class ReportedListingAdmin(BaseModerationAdmin):

    def get_queryset(self, request):

        return super().get_queryset(request).filter(
            is_reported=True
        )

# ==========================================
# SECTION 13 END
# ==========================================


# ==========================================
# SECTION 14 START
# End File
# ==========================================

# ==========================================
# SECTION 14 END
# ==========================================