# ==========================================
# MyCarMarket Australia
# Version: v2.2.1
# File: services/urls.py
# Description:
# Car Services URL configuration with:
# - Public service listings
# - Service detail pages
# - Service enquiry submission
# - Service listing creation
# - User service management
# - Unnamespaced URL names for compatibility
# ==========================================


# ==========================================
# SECTION 1 START
# Imports
# ==========================================

from django.urls import path

from services import views

# ==========================================
# SECTION 1 END
# Imports
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 2 START
# Service URLs
# ==========================================

urlpatterns = [

    path(
        "",
        views.service_list,
        name="service_list",
    ),

    path(
        "list-your-service/",
        views.create_service,
        name="create_service",
    ),

    path(
        "submission-success/",
        views.service_submission_success,
        name="service_submission_success",
    ),

    path(
        "my-listings/",
        views.my_service_listings,
        name="my_service_listings",
    ),

    path(
        "<slug:slug>/edit/",
        views.edit_service,
        name="edit_service",
    ),

    path(
        "<slug:slug>/preview/",
        views.service_owner_preview,
        name="service_owner_preview",
    ),

    path(
        "<slug:slug>/delete/",
        views.delete_service,
        name="delete_service",
    ),

    path(
        "<slug:slug>/enquiry/",
        views.submit_service_enquiry,
        name="submit_service_enquiry",
    ),

    path(
        "<slug:slug>/",
        views.service_detail,
        name="service_detail",
    ),

]

# ==========================================
# SECTION 2 END
# Service URLs
# ==========================================