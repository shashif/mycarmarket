# ==========================================
# MyCarMarket
# Version: v1.0.1
# File: core/models.py
# Homepage Hero Settings + Alternate Banner Ads
# ==========================================

from django.db import models


class SiteSettings(models.Model):

    hero_image = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True
    )

    hero_title = models.CharField(
        max_length=200,
        blank=True
    )

    hero_subtitle = models.CharField(
        max_length=300,
        blank=True
    )

    alternate_google_banner_ad = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True
    )

    alternate_google_banner_link = models.URLField(
        blank=True
    )

    def __str__(self):
        return "Homepage Settings"

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"