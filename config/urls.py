# ==========================================
# MyCarMarket
# Version: v1.4.1
# File: config/urls.py
# Sitemap + Robots + Static Media + Custom 404 + Favicon Fix
# ==========================================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView

from vehicles.sitemaps import CarSitemap
from core.views_robots import robots_txt


sitemaps = {
    'cars': CarSitemap,
}


urlpatterns = [
    path(
        'favicon.ico',
        RedirectView.as_view(
            url='/static/favicon/favicon.ico',
            permanent=True
        ),
    ),

    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('cars/', include('vehicles.urls')),

    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),

    path(
        'robots.txt',
        robots_txt,
        name='robots_txt'
    ),
]


# ==========================================
# CUSTOM ERROR PAGES
# ==========================================

handler404 = 'core.views.custom_404'


# ==========================================
# LOCAL DEVELOPMENT MEDIA / STATIC
# ==========================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.BASE_DIR / 'static'
    )