# ==========================================
# MyCarMarket
# Version: v0.8.2
# File: vehicles/sitemaps.py
# Car Sitemap URLs
# ==========================================

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from vehicles.models import Car


class CarSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Car.objects.filter(
            is_approved=True,
            is_active=True
        )

    def location(self, obj):
        return reverse(
            'car_detail',
            kwargs={
                'slug': obj.slug
            }
        )

    def lastmod(self, obj):
        return obj.created_at