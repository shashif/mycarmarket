# ==========================================
# MyCarMarket Australia
# Version: v2.1.0
# File: rentals/urls.py
# Description:
# Rental listing, detail, create and enquiry URLs.
# ==========================================

from django.urls import path

from rentals import views


# ==========================================
# SECTION 1 START
# Rental URLs
# ==========================================

urlpatterns = [

    path(
        "",
        views.rental_list,
        name="rental_list",
    ),

    path(
        "list-your-car/",
        views.create_rental,
        name="create_rental",
    ),

    path(
        "enquiry/<int:pk>/submit/",
        views.submit_rental_enquiry,
        name="submit_rental_enquiry",
    ),

    path(
        "<slug:slug>/",
        views.rental_detail,
        name="rental_detail",
    ),

]


# ==========================================
# SECTION 1 END
# Rental URLs
# ==========================================