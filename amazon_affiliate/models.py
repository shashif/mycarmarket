# ==========================================
# MyCarMarket
# Version: v1.14.0
# File: amazon_affiliate/models.py
# Description:
# Amazon Accessories Store
# Categories + Products + Store ID Auto Tag
# ==========================================

from django.db import models
from django.utils.text import slugify


class AmazonAffiliateSettings(models.Model):

    store_id = models.CharField(
        max_length=100,
        default="mycarmarketau-22",
        help_text="Your Amazon Associates Store ID / Tracking ID."
    )

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Amazon Affiliate Setting"
        verbose_name_plural = "Amazon Affiliate Settings"

    def __str__(self):
        return self.store_id


class AmazonCategory(models.Model):

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    short_description = models.CharField(
        max_length=220,
        blank=True
    )

    image = models.ImageField(
        upload_to="amazon_affiliate/categories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Amazon Category"
        verbose_name_plural = "Amazon Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class AmazonProduct(models.Model):

    BODY_TYPE_CHOICES = [
        ("all", "All"),
        ("suv", "SUV"),
        ("sedan", "Sedan"),
        ("hatchback", "Hatchback"),
        ("wagon", "Wagon"),
        ("ute", "Ute"),
        ("van", "Van"),
        ("coupe", "Coupe"),
        ("convertible", "Convertible"),
        ("4wd", "4WD"),
        ("ev", "Electric Vehicle"),
        ("hybrid", "Hybrid"),
    ]

    amazon_product_url = models.URLField(
        blank=True,
        help_text="Paste normal Amazon product URL here."
    )

    amazon_affiliate_url = models.URLField(
        blank=True,
        help_text="Auto generated using your Store ID, but editable."
    )

    asin = models.CharField(max_length=30, blank=True)

    title = models.CharField(
        max_length=180,
        blank=True,
        default="Amazon Car Accessory"
    )

    brand = models.CharField(max_length=100, blank=True)

    short_description = models.CharField(
        max_length=240,
        blank=True
    )

    product_category = models.ForeignKey(
        AmazonCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products"
    )

    category = models.CharField(
        max_length=40,
        default="general",
        blank=True,
        help_text="Old category field. Kept for migration safety."
    )

    body_type = models.CharField(
        max_length=30,
        choices=BODY_TYPE_CHOICES,
        default="all"
    )

    image = models.ImageField(
        upload_to="amazon_affiliate/products/",
        blank=True,
        null=True
    )

    button_text = models.CharField(
        max_length=60,
        default="View on Amazon"
    )

    click_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    display_order = models.PositiveIntegerField(default=0)

    last_synced_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "title"]
        verbose_name = "Amazon Product"
        verbose_name_plural = "Amazon Products"

    def __str__(self):
        return self.title or "Amazon Product"

    def save(self, *args, **kwargs):

        if self.amazon_product_url and not self.amazon_affiliate_url:

            affiliate_settings = AmazonAffiliateSettings.objects.filter(
                is_active=True
            ).first()

            if affiliate_settings and affiliate_settings.store_id:
                separator = "&" if "?" in self.amazon_product_url else "?"

                self.amazon_affiliate_url = (
                    f"{self.amazon_product_url}"
                    f"{separator}"
                    f"tag={affiliate_settings.store_id}"
                )

        super().save(*args, **kwargs)