# ==========================================
# MyCarMarket
# Version: v1.0.2
# File: core/models.py
# Homepage Hero + Custom / Google Ad Switch
# ==========================================

from django.db import models


class SiteSettings(models.Model):

    # ==========================================
    # AD TYPE CHOICES
    # ==========================================

    AD_TYPE_CHOICES = [
        ('custom', 'Custom Image Ad'),
        ('google', 'Google AdSense Ad'),
    ]

    # ==========================================
    # HOMEPAGE HERO SETTINGS
    # ==========================================

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

    # ==========================================
    # HOMEPAGE AD SETTINGS
    # ==========================================

    homepage_ad_type = models.CharField(
        max_length=20,
        choices=AD_TYPE_CHOICES,
        default='custom'
    )

    alternate_google_banner_ad = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True
    )

    alternate_google_banner_link = models.URLField(
        blank=True
    )

    google_adsense_code = models.TextField(
        blank=True
    )

    # ==========================================
    # MODEL DISPLAY
    # ==========================================

    def __str__(self):
        return "Homepage Settings"

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"