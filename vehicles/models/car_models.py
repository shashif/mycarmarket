# ==========================================
# MyCarMarket
# Version: v1.0.5
# File: vehicles/models/car_models.py
# Car + Car Image Models
# ==========================================

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


# ==========================================
# CAR CHOICES START
# ==========================================

BODY_TYPE_CHOICES = [
    ('Sedan', 'Sedan'),
    ('SUV', 'SUV'),
    ('Hatchback', 'Hatchback'),
    ('Ute', 'Ute'),
    ('Coupe', 'Coupe'),
    ('Convertible', 'Convertible'),
    ('Wagon', 'Wagon'),
    ('Van', 'Van'),
    ('Other', 'Other'),
]

TRANSMISSION_CHOICES = [
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
]

FUEL_TYPE_CHOICES = [
    ('Petrol', 'Petrol'),
    ('Diesel', 'Diesel'),
    ('Hybrid', 'Hybrid'),
    ('Electric', 'Electric'),
    ('LPG', 'LPG'),
    ('Other', 'Other'),
]

STATE_CHOICES = [
    ('VIC', 'Victoria'),
    ('NSW', 'New South Wales'),
    ('QLD', 'Queensland'),
    ('SA', 'South Australia'),
    ('WA', 'Western Australia'),
    ('TAS', 'Tasmania'),
    ('ACT', 'Australian Capital Territory'),
    ('NT', 'Northern Territory'),
]

# ==========================================
# CAR CHOICES END
# ==========================================


# ==========================================
# CAR MODEL START
# ==========================================

class Car(models.Model):

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cars',
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    kilometres = models.PositiveIntegerField()

    body_type = models.CharField(
        max_length=50,
        choices=BODY_TYPE_CHOICES,
        blank=True
    )

    transmission = models.CharField(
        max_length=50,
        choices=TRANSMISSION_CHOICES,
        blank=True
    )

    fuel_type = models.CharField(
        max_length=50,
        choices=FUEL_TYPE_CHOICES,
        blank=True
    )

    state = models.CharField(
        max_length=10,
        choices=STATE_CHOICES,
        blank=True
    )

    suburb = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    seller_name = models.CharField(max_length=100, blank=True)
    seller_email = models.EmailField(blank=True)
    seller_phone = models.CharField(max_length=30, blank=True)

    is_featured = models.BooleanField(default=False)
    featured_until = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_verified_listing = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # ==========================================
    # SLUG AUTO GENERATION
    # ==========================================

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(
                f"{self.year}-{self.make}-{self.model}-{self.title}"
            )

            if not base_slug:
                base_slug = "car-listing"

            slug = base_slug
            counter = 1

            while Car.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    # ==========================================
    # DISPLAY HELPERS
    # ==========================================

    def display_location(self):
        if self.suburb and self.state:
            return f"{self.suburb}, {self.state}"

        if self.suburb:
            return self.suburb

        if self.state:
            return self.state

        return ""

    def primary_image(self):
        primary = self.images.filter(is_primary=True).first()

        if primary:
            return primary.image.url

        first_image = self.images.first()

        if first_image:
            return first_image.image.url

        return None

    # ==========================================
    # SELLER / DEALER HELPERS
    # ==========================================

    def seller_is_verified(self):
        if self.seller and hasattr(self.seller, 'dealer_profile'):
            return self.seller.dealer_profile.is_verified

        return False

    def seller_verified_badge(self):
        if self.seller and hasattr(self.seller, 'dealer_profile'):
            return self.seller.dealer_profile.verified_badge()

        return ''

    def seller_package_badge(self):
        if self.seller and hasattr(self.seller, 'dealer_profile'):
            return self.seller.dealer_profile.package_badge()

        return 'Private Seller'

    def seller_business_name(self):
        if self.seller and hasattr(self.seller, 'dealer_profile'):
            profile = self.seller.dealer_profile

            if profile.business_name:
                return profile.business_name

        return self.seller_name or 'Private Seller'

    def seller_is_featured_dealer(self):
        if self.seller and hasattr(self.seller, 'dealer_profile'):
            return self.seller.dealer_profile.is_featured_dealer

        return False

    def __str__(self):
        return self.title

# ==========================================
# CAR MODEL END
# ==========================================


# ==========================================
# CAR IMAGE MODEL START
# Auto Image Compression System
# ==========================================

class CarImage(models.Model):

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='cars/')
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def save(self, *args, **kwargs):

        if self.image:
            try:
                img = Image.open(self.image)

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                MAX_WIDTH = 1400
                MAX_HEIGHT = 1000
                JPEG_QUALITY = 75

                img.thumbnail(
                    (MAX_WIDTH, MAX_HEIGHT),
                    Image.Resampling.LANCZOS
                )

                buffer = BytesIO()

                img.save(
                    buffer,
                    format='JPEG',
                    quality=JPEG_QUALITY,
                    optimize=True
                )

                original_name = os.path.splitext(self.image.name)[0]
                new_file_name = f"{original_name}.jpg"

                self.image.save(
                    new_file_name,
                    ContentFile(buffer.getvalue()),
                    save=False
                )

            except Exception:
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.car.title}"

# ==========================================
# CAR IMAGE MODEL END
# ==========================================