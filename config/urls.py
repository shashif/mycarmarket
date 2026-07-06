# ==========================================
# MyCarMarket
# Version: v1.10.3
# File: config/urls.py
# Description: Sitemap + Robots + Static Media + Custom Error Pages + Favicon + Bing Verification + Reviews URLs
# ==========================================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from django.views.static import serve

from vehicles.sitemaps import CarSitemap
from reviews.sitemaps import ReviewSitemap
from core.views_robots import robots_txt


sitemaps = {
    'cars': CarSitemap,
    'reviews': ReviewSitemap,
}


urlpatterns = [
    path(
        'BingSiteAuth.xml',
        serve,
        {
            'document_root': settings.BASE_DIR,
            'path': 'BingSiteAuth.xml',
        },
    ),

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
    path('reviews/', include('reviews.urls')),

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

handler403 = 'core.views.custom_403'
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'


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