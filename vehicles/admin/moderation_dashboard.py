# ==========================================
# MyCarMarket Australia
# Version: v2.3.0
# File: vehicles/admin/moderation_dashboard.py
# Location: vehicles/admin/moderation_dashboard.py
# Description:
# Global Moderation Center integration for:
# - Cars
# - Rental Cars
# - Car Services
# Features:
# - Unified moderation statistics
# - Combined pending queue
# - Rental quick approve/reject actions
# - Service quick approve/reject actions
# - Reuses each app's registered ModelAdmin moderation actions
# - Preserves the existing Cars moderation workflow
# Last Updated: 24 Jul 2026
# ==========================================


# ==========================================
# SECTION 01 START
# Imports
# ==========================================

from itertools import chain

from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils import timezone

from rentals.models import RentalCar
from services.models import CarService
from vehicles.models import Car

# ==========================================
# SECTION 01 END
# ==========================================


# ==========================================
# SECTION 02 START
# Global Moderation Dashboard Mixin
# ==========================================

class GlobalModerationDashboardMixin:
    """
    Adds Rentals and Services to the existing Cars moderation dashboard.

    This mixin does not replace the existing Cars moderation logic. It extends
    the current ModerationDashboardAdmin and delegates Rental and Service
    approval/rejection operations to their already-registered ModelAdmin
    classes.
    """

    change_list_template = "admin/vehicles/moderation_dashboard.html"

    global_pending_limit = 30
    dashboard_recent_limit = 10

    # ==========================================
    # SECTION 03 START
    # Dashboard Context
    # ==========================================

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        car_counts = self._get_status_counts(Car)
        rental_counts = self._get_status_counts(RentalCar)
        service_counts = self._get_status_counts(CarService)

        combined_pending = self._build_combined_pending_queue(
            limit=self.global_pending_limit
        )

        total_pending = (
            car_counts["pending"]
            + rental_counts["pending"]
            + service_counts["pending"]
        )

        total_approved = (
            car_counts["approved"]
            + rental_counts["approved"]
            + service_counts["approved"]
        )

        total_rejected = (
            car_counts["rejected"]
            + rental_counts["rejected"]
            + service_counts["rejected"]
        )

        extra_context.update(
            {
                # Global totals
                "global_total_pending": total_pending,
                "global_total_approved": total_approved,
                "global_total_rejected": total_rejected,

                # Cars
                "car_pending_count": car_counts["pending"],
                "car_approved_count": car_counts["approved"],
                "car_rejected_count": car_counts["rejected"],
                "car_suspended_count": car_counts["suspended"],

                # Rentals
                "rental_pending_count": rental_counts["pending"],
                "rental_approved_count": rental_counts["approved"],
                "rental_rejected_count": rental_counts["rejected"],

                # Services
                "service_pending_count": service_counts["pending"],
                "service_approved_count": service_counts["approved"],
                "service_rejected_count": service_counts["rejected"],

                # Combined queue
                "combined_pending_listings": combined_pending,

                # Direct admin list links
                "car_admin_url": reverse(
                    "admin:vehicles_car_changelist"
                ),
                "rental_admin_url": reverse(
                    "admin:rentals_rentalcar_changelist"
                ),
                "service_admin_url": reverse(
                    "admin:services_carservice_changelist"
                ),

                # Filtered admin links
                "car_pending_admin_url": self._filtered_changelist_url(
                    "admin:vehicles_car_changelist",
                    moderation_status="pending",
                ),
                "rental_pending_admin_url": self._filtered_changelist_url(
                    "admin:rentals_rentalcar_changelist",
                    moderation_status="pending",
                ),
                "service_pending_admin_url": self._filtered_changelist_url(
                    "admin:services_carservice_changelist",
                    moderation_status="pending",
                ),
            }
        )

        return super().changelist_view(
            request,
            extra_context=extra_context,
        )

    def _get_status_counts(self, model):
        queryset = model.objects.all()

        counts = {
            "pending": queryset.filter(
                moderation_status="pending"
            ).count(),
            "approved": queryset.filter(
                moderation_status="approved"
            ).count(),
            "rejected": queryset.filter(
                moderation_status="rejected"
            ).count(),
            "suspended": 0,
        }

        status_values = {
            value
            for value, _label in model._meta.get_field(
                "moderation_status"
            ).choices
        }

        if "suspended" in status_values:
            counts["suspended"] = queryset.filter(
                moderation_status="suspended"
            ).count()

        return counts

    # ==========================================
    # SECTION 03 END
    # ==========================================


    # ==========================================
    # SECTION 04 START
    # Combined Pending Queue
    # ==========================================

    def _build_combined_pending_queue(self, limit=30):
        cars = [
            self._normalise_car(car)
            for car in Car.objects.filter(
                moderation_status="pending"
            ).order_by("-created_at")[:limit]
        ]

        rentals = [
            self._normalise_rental(rental)
            for rental in RentalCar.objects.filter(
                moderation_status="pending"
            ).order_by("-created_at")[:limit]
        ]

        services = [
            self._normalise_service(service)
            for service in CarService.objects.filter(
                moderation_status="pending"
            ).order_by("-created_at")[:limit]
        ]

        combined = sorted(
            chain(cars, rentals, services),
            key=lambda item: item["created_at"],
            reverse=True,
        )

        return combined[:limit]

    def _normalise_car(self, car):
        image_url = ""

        try:
            primary_image = car.images.filter(
                is_primary=True
            ).first() or car.images.first()

            if primary_image and primary_image.image:
                image_url = primary_image.image.url
        except Exception:
            image_url = ""

        return {
            "listing_type": "car",
            "listing_type_label": "Car",
            "listing_type_icon": "🚗",
            "object_id": car.pk,
            "title": car.title,
            "owner": self._first_non_empty(
                getattr(car, "seller_name", ""),
                getattr(
                    getattr(car, "seller", None),
                    "get_full_name",
                    lambda: "",
                )(),
                getattr(
                    getattr(car, "seller", None),
                    "username",
                    "",
                ),
                getattr(car, "seller_email", ""),
                "Unknown seller",
            ),
            "location": self._first_non_empty(
                getattr(car, "suburb", ""),
                getattr(car, "state", ""),
                "",
            ),
            "created_at": car.created_at,
            "image_url": image_url,
            "change_url": reverse(
                "admin:vehicles_car_change",
                args=[car.pk],
            ),
            "approve_url": self._safe_reverse(
                "admin:vehicles_pendinglisting_quick_approve",
                args=[car.pk],
            ),
            "reject_url": self._safe_reverse(
                "admin:vehicles_pendinglisting_quick_reject",
                args=[car.pk],
            ),
        }

    def _normalise_rental(self, rental):
        image_url = ""

        try:
            primary_image = rental.primary_image

            if primary_image and primary_image.image:
                image_url = primary_image.image.url
        except Exception:
            image_url = ""

        return {
            "listing_type": "rental",
            "listing_type_label": "Rental",
            "listing_type_icon": "🔑",
            "object_id": rental.pk,
            "title": rental.title,
            "owner": self._first_non_empty(
                getattr(rental, "owner_name", ""),
                getattr(
                    getattr(rental, "posted_by", None),
                    "get_full_name",
                    lambda: "",
                )(),
                getattr(
                    getattr(rental, "posted_by", None),
                    "username",
                    "",
                ),
                getattr(rental, "owner_email", ""),
                "Unknown owner",
            ),
            "location": self._first_non_empty(
                getattr(rental, "location", ""),
                getattr(rental, "suburb", ""),
                getattr(rental, "state", ""),
                "",
            ),
            "created_at": rental.created_at,
            "image_url": image_url,
            "change_url": reverse(
                "admin:rentals_rentalcar_change",
                args=[rental.pk],
            ),
            "approve_url": reverse(
                "admin:global_moderation_rental_approve",
                args=[rental.pk],
            ),
            "reject_url": reverse(
                "admin:global_moderation_rental_reject",
                args=[rental.pk],
            ),
        }

    def _normalise_service(self, service):
        image_url = ""

        try:
            primary_image = service.primary_image

            if primary_image and primary_image.image:
                image_url = primary_image.image.url
        except Exception:
            image_url = ""

        return {
            "listing_type": "service",
            "listing_type_label": "Service",
            "listing_type_icon": "🛠️",
            "object_id": service.pk,
            "title": service.title,
            "owner": self._first_non_empty(
                getattr(service, "business_name", ""),
                getattr(service, "provider_name", ""),
                getattr(
                    getattr(service, "posted_by", None),
                    "get_full_name",
                    lambda: "",
                )(),
                getattr(
                    getattr(service, "posted_by", None),
                    "username",
                    "",
                ),
                getattr(service, "provider_email", ""),
                "Unknown provider",
            ),
            "location": self._first_non_empty(
                getattr(service, "location", ""),
                getattr(service, "suburb", ""),
                getattr(service, "state", ""),
                "",
            ),
            "created_at": service.created_at,
            "image_url": image_url,
            "change_url": reverse(
                "admin:services_carservice_change",
                args=[service.pk],
            ),
            "approve_url": reverse(
                "admin:global_moderation_service_approve",
                args=[service.pk],
            ),
            "reject_url": reverse(
                "admin:global_moderation_service_reject",
                args=[service.pk],
            ),
        }

    # ==========================================
    # SECTION 04 END
    # ==========================================


    # ==========================================
    # SECTION 05 START
    # Global Quick Action URLs
    # ==========================================

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "rental/<int:object_id>/quick-approve/",
                self.admin_site.admin_view(
                    self.quick_approve_rental
                ),
                name="global_moderation_rental_approve",
            ),
            path(
                "rental/<int:object_id>/quick-reject/",
                self.admin_site.admin_view(
                    self.quick_reject_rental
                ),
                name="global_moderation_rental_reject",
            ),
            path(
                "service/<int:object_id>/quick-approve/",
                self.admin_site.admin_view(
                    self.quick_approve_service
                ),
                name="global_moderation_service_approve",
            ),
            path(
                "service/<int:object_id>/quick-reject/",
                self.admin_site.admin_view(
                    self.quick_reject_service
                ),
                name="global_moderation_service_reject",
            ),
        ]

        return custom_urls + urls

    # ==========================================
    # SECTION 05 END
    # ==========================================


    # ==========================================
    # SECTION 06 START
    # Rental Quick Actions
    # ==========================================

    def quick_approve_rental(self, request, object_id):
        rental = get_object_or_404(
            RentalCar,
            pk=object_id,
        )

        self._require_model_change_permission(
            request,
            RentalCar,
            rental,
        )

        rental_admin = self._get_registered_model_admin(
            RentalCar
        )

        if (
            rental.moderation_status == "approved"
            and rental.is_approved
        ):
            messages.info(
                request,
                f"{rental.title} is already approved.",
            )
        else:
            rental_admin.approve_selected_rentals(
                request,
                RentalCar.objects.filter(pk=rental.pk),
            )

        return self._return_to_previous_page(request)

    def quick_reject_rental(self, request, object_id):
        rental = get_object_or_404(
            RentalCar,
            pk=object_id,
        )

        self._require_model_change_permission(
            request,
            RentalCar,
            rental,
        )

        rental_admin = self._get_registered_model_admin(
            RentalCar
        )

        if rental.moderation_status == "rejected":
            messages.info(
                request,
                f"{rental.title} is already rejected.",
            )
        else:
            rental_admin.reject_selected_rentals(
                request,
                RentalCar.objects.filter(pk=rental.pk),
            )

        return self._return_to_previous_page(request)

    # ==========================================
    # SECTION 06 END
    # ==========================================


    # ==========================================
    # SECTION 07 START
    # Service Quick Actions
    # ==========================================

    def quick_approve_service(self, request, object_id):
        service = get_object_or_404(
            CarService,
            pk=object_id,
        )

        self._require_model_change_permission(
            request,
            CarService,
            service,
        )

        service_admin = self._get_registered_model_admin(
            CarService
        )

        if (
            service.moderation_status == "approved"
            and service.is_approved
        ):
            messages.info(
                request,
                f"{service.title} is already approved.",
            )
        else:
            service_admin.approve_selected_services(
                request,
                CarService.objects.filter(pk=service.pk),
            )

        return self._return_to_previous_page(request)

    def quick_reject_service(self, request, object_id):
        service = get_object_or_404(
            CarService,
            pk=object_id,
        )

        self._require_model_change_permission(
            request,
            CarService,
            service,
        )

        service_admin = self._get_registered_model_admin(
            CarService
        )

        if service.moderation_status == "rejected":
            messages.info(
                request,
                f"{service.title} is already rejected.",
            )
        else:
            service_admin.reject_selected_services(
                request,
                CarService.objects.filter(pk=service.pk),
            )

        return self._return_to_previous_page(request)

    # ==========================================
    # SECTION 07 END
    # ==========================================


    # ==========================================
    # SECTION 08 START
    # Utility Methods
    # ==========================================

    def _get_registered_model_admin(self, model):
        model_admin = self.admin_site._registry.get(model)

        if model_admin is None:
            raise RuntimeError(
                f"{model.__name__} is not registered in Django admin."
            )

        return model_admin

    def _require_model_change_permission(
        self,
        request,
        model,
        obj,
    ):
        model_admin = self._get_registered_model_admin(model)

        if not model_admin.has_change_permission(
            request,
            obj,
        ):
            raise PermissionDenied

    def _return_to_previous_page(self, request):
        return redirect(
            request.META.get(
                "HTTP_REFERER",
                reverse(
                    "admin:vehicles_moderationdashboard_changelist"
                ),
            )
        )

    def _filtered_changelist_url(
        self,
        url_name,
        **filters,
    ):
        base_url = reverse(url_name)

        query_string = "&".join(
            f"{key}__exact={value}"
            for key, value in filters.items()
        )

        if not query_string:
            return base_url

        return f"{base_url}?{query_string}"

    def _safe_reverse(self, url_name, args=None):
        try:
            return reverse(
                url_name,
                args=args or [],
            )
        except Exception:
            return ""

    @staticmethod
    def _first_non_empty(*values):
        for value in values:
            if value not in (None, ""):
                return str(value)

        return ""

    # ==========================================
    # SECTION 08 END
    # ==========================================


# ==========================================
# SECTION 02 END
# ==========================================


# ==========================================
# SECTION 09 START
# End File
# ==========================================

# ==========================================
# SECTION 09 END
# ==========================================
