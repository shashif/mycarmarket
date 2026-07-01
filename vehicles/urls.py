# ==========================================
# MyCarMarket
# Version: v1.5.5
# File: vehicles/urls.py
# Description: SEO URLs + Dealer Dashboard + Reviews + Payments + AI Price Estimation
# ==========================================

from django.urls import path
from . import views
from vehicles.views.price_estimate_views import ai_price_estimate


urlpatterns = [

    path(
        '',
        views.car_list,
        name='car_list'
    ),

    path(
        'car/<slug:slug>/',
        views.car_detail,
        name='car_detail'
    ),

    # ==========================================
    # AI Smart Price Estimation API
    # ==========================================

    path(
        'ai-price-estimate/',
        ai_price_estimate,
        name='ai_price_estimate'
    ),

    path(
        'api/price-suggestion/',
        views.price_suggestion_api,
        name='price_suggestion_api'
    ),

    # ==========================================
    # Dealer Enquiry System
    # ==========================================

    path(
        'dealer/enquiries/',
        views.dealer_enquiries,
        name='dealer_enquiries'
    ),

    path(
        'car/<slug:slug>/favourite/',
        views.toggle_favourite,
        name='toggle_favourite'
    ),

    path(
        'saved-cars/',
        views.saved_cars,
        name='saved_cars'
    ),

    # ==========================================
    # Dealer Dashboard + Dealer Profile
    # ==========================================

    path(
        'dealer/dashboard/',
        views.dealer_dashboard,
        name='dealer_dashboard'
    ),

    path(
        'dealer/profile/edit/',
        views.edit_dealer_profile,
        name='edit_dealer_profile'
    ),

    # ==========================================
    # Dealer Reviews
    # ==========================================

    path(
        'dealer/<str:username>/review/add/',
        views.add_review,
        name='add_dealer_review'
    ),

    path(
        'dealer/review/<int:review_id>/edit/',
        views.edit_review,
        name='edit_dealer_review'
    ),

    path(
        'dealer/review/<int:review_id>/delete/',
        views.delete_review,
        name='delete_dealer_review'
    ),

    path(
        'dealer/<str:username>/',
        views.dealer_detail,
        name='dealer_detail'
    ),

    path(
        'dealer-packages/',
        views.dealer_packages,
        name='dealer_packages'
    ),

    path(
        'dealer/package/select/',
        views.dealer_package_select,
        name='dealer_package_select'
    ),

    # ==========================================
    # Stripe Payment URLs
    # ==========================================

    path(
        'checkout/<str:package_name>/',
        views.create_checkout_session,
        name='create_checkout_session'
    ),

    path(
        'payment-success/',
        views.payment_success,
        name='payment_success'
    ),

    path(
        'payment-cancelled/',
        views.payment_cancelled,
        name='payment_cancelled'
    ),

    path(
        'stripe/webhook/',
        views.stripe_webhook,
        name='stripe_webhook'
    ),

    # ==========================================
    # Car Management URLs
    # ==========================================

    path(
        'create/',
        views.create_car,
        name='create_car'
    ),

    path(
        'my-listings/',
        views.my_listings,
        name='my_listings'
    ),

    path(
        'edit/<int:pk>/',
        views.edit_car,
        name='edit_car'
    ),

    path(
        'delete/<int:pk>/',
        views.delete_car,
        name='delete_car'
    ),
]