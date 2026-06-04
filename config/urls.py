# ==========================================
# MyCarMarket
# Version: v0.3.2 - Media URL Fix
# File: config/urls.py
# ==========================================

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cars/', include('vehicles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)