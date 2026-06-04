# ==========================================
# MyCarMarket
# Version: v0.3.6 - View Counter + Trust Fields
# File: vehicles/models.py
# ==========================================

from django.db import models


class Car(models.Model):

    BODY_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Hatchback', 'Hatchback'),
        ('Ute', 'Ute'),
        ('Wagon', 'Wagon'),
        ('Coupe', 'Coupe'),
        ('Convertible', 'Convertible'),
        ('Van', 'Van'),
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
    ]

    title = models.CharField(max_length=200)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    kilometres = models.PositiveIntegerField(default=0)

    location = models.CharField(max_length=150, blank=True)

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

    body_type = models.CharField(
        max_length=50,
        choices=BODY_TYPE_CHOICES,
        blank=True
    )

    description = models.TextField(blank=True)

    seller_name = models.CharField(max_length=150, blank=True)
    seller_email = models.EmailField(blank=True)
    seller_phone = models.CharField(max_length=30, blank=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_verified_listing = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.car.title} Image"


class Enquiry(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='enquiries')

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry for {self.car.title} by {self.name}"