# ==========================================
# MyCarMarket Australia
# Version: v2.2.0
# File: config/urls.py
# Description:
# Project URL Configuration
# - Core
# - Vehicles
# - Rentals
# - Services
# - Reviews
# - Amazon Accessories
# - Sitemap
# - Robots
# - Static & Media
# ==========================================

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from django.views.static import serve

from vehicles.sitemaps import CarSitemap
from reviews.sitemaps import ReviewSitemap
from core.views_robots import robots_txt


# ==========================================
# Sitemaps
# ==========================================

sitemaps = {
    "cars": CarSitemap,
    "reviews": ReviewSitemap,
}


# ==========================================
# URL Patterns
# ==========================================

urlpatterns = [

    path(
        "BingSiteAuth.xml",
        serve,
        {
            "document_root": settings.BASE_DIR,
            "path": "BingSiteAuth.xml",
        },
    ),

    path(
        "favicon.ico",
        RedirectView.as_view(
            url="/static/favicon/favicon.ico",
            permanent=True,
        ),
    ),

    path(
        "admin/",
        admin.site.urls,
    ),

    # ==========================================
    # Core
    # ==========================================

    path(
        "",
        include("core.urls"),
    ),

    # ==========================================
    # Amazon Accessories
    # ==========================================

    path(
        "",
        include("amazon_affiliate.urls"),
    ),

    # ==========================================
    # Vehicle Marketplace
    # ==========================================

    path(
        "cars/",
        include("vehicles.urls"),
    ),

    # ==========================================
    # Rentals
    # ==========================================

    path(
        "rentals/",
        include("rentals.urls"),
    ),

    # ==========================================
    # Car Services
    # ==========================================

    path(
        "services/",
        include("services.urls"),
    ),

    # ==========================================
    # Reviews
    # ==========================================

    path(
        "reviews/",
        include("reviews.urls"),
    ),

    # ==========================================
    # Accounts
    # ==========================================

    path(
        "accounts/",
        include("accounts.urls"),
    ),

    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),

    # ==========================================
    # Sitemap
    # ==========================================

    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": sitemaps,
        },
        name="django.contrib.sitemaps.views.sitemap",
    ),

    # ==========================================
    # Robots
    # ==========================================

    path(
        "robots.txt",
        robots_txt,
        name="robots_txt",
    ),
]


# ==========================================
# Custom Error Pages
# ==========================================

handler403 = "core.views.custom_403"

handler404 = "core.views.custom_404"

handler500 = "core.views.custom_500"


# ==========================================
# Local Development
# ==========================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.BASE_DIR / "static",
    )