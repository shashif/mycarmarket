# ==========================================
# MyCarMarket
# Version: v0.8.6
# File: vehicles/models.py
# SEO Slug + Enquiry + Favourite Cars + Dealer Branding + Dealer Packages
# ==========================================

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


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


class DealerProfile(models.Model):
    PACKAGE_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter - $99 AUD'),
        ('professional', 'Professional - $299 AUD'),
        ('premium', 'Premium - $599 AUD'),
        ('enterprise', 'Enterprise - $999 AUD'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dealer_profile'
    )

    business_name = models.CharField(max_length=150, blank=True)
    business_description = models.TextField(blank=True)

    logo = models.ImageField(
        upload_to='dealer_logos/',
        blank=True,
        null=True
    )

    banner = models.ImageField(
        upload_to='dealer_banners/',
        blank=True,
        null=True
    )

    website = models.URLField(blank=True)
    business_phone = models.CharField(max_length=30, blank=True)
    business_email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)

    package = models.CharField(
        max_length=20,
        choices=PACKAGE_CHOICES,
        default='free'
    )

    is_dealer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    package_active = models.BooleanField(default=True)
    is_featured_dealer = models.BooleanField(default=False)

    max_listings = models.PositiveIntegerField(default=3)
    featured_ads_allowed = models.PositiveIntegerField(default=0)
    priority_support = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def package_badge(self):
        if self.package == 'enterprise':
            return '👑 Enterprise Dealer'
        if self.package == 'premium':
            return '⭐ Premium Dealer'
        if self.package == 'professional':
            return '🏢 Professional Dealer'
        if self.package == 'starter':
            return '🚗 Starter Dealer'
        return 'Basic Seller'

    def verified_badge(self):
        if self.is_verified:
            return '✔ Verified Dealer'
        return ''

    def __str__(self):
        name = self.business_name or self.user.username
        return f"{name} - {self.package}"


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

    body_type = models.CharField(max_length=50, choices=BODY_TYPE_CHOICES, blank=True)
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES, blank=True)
    fuel_type = models.CharField(max_length=50, choices=FUEL_TYPE_CHOICES, blank=True)

    state = models.CharField(max_length=10, choices=STATE_CHOICES, blank=True)
    suburb = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    seller_name = models.CharField(max_length=100, blank=True)
    seller_email = models.EmailField(blank=True)
    seller_phone = models.CharField(max_length=30, blank=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified_listing = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.year}-{self.make}-{self.model}-{self.title}")

            if not base_slug:
                base_slug = "car-listing"

            slug = base_slug
            counter = 1

            while Car.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

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

    def __str__(self):
        return f"Image for {self.car.title}"


class Enquiry(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Enquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.car.title}"


class FavouriteCar(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite_cars'
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='favourited_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} saved {self.car.title}"