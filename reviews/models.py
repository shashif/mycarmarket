from django.db import models

# Create your models here.
# ==========================================
# MyCarMarket
# Version: v1.10.3
# File: reviews/models.py
# Description: Professional Car Review Model for SEO Content Hub
# ==========================================

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# ==========================================
# SECTION 01: CAR REVIEW MODEL
# START
# ==========================================

class CarReview(models.Model):

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    make = models.CharField(
        max_length=100,
        help_text='Example: Toyota, Ford, Mazda'
    )

    model = models.CharField(
        max_length=100,
        help_text='Example: Corolla, Ranger, CX-5'
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Optional. Example: 2023'
    )

    body_type = models.CharField(
        max_length=100,
        blank=True,
        help_text='Example: SUV, Sedan, Hatchback, Ute'
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=8.0,
        help_text='Example: 8.5'
    )

    hero_image = models.ImageField(
        upload_to='reviews/',
        blank=True,
        null=True
    )

    summary = models.TextField(
        help_text='Short SEO-friendly intro / quick verdict.'
    )

    pros = models.TextField(
        blank=True,
        help_text='One point per line.'
    )

    cons = models.TextField(
        blank=True,
        help_text='One point per line.'
    )

    content = models.TextField(
        help_text='Full review article content.'
    )

    faq = models.TextField(
        blank=True,
        help_text='Optional FAQ content. Add question and answer format.'
    )

    meta_title = models.CharField(
        max_length=255,
        blank=True
    )

    meta_description = models.CharField(
        max_length=320,
        blank=True
    )

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Car Review'
        verbose_name_plural = 'Car Reviews'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.year:
                base_slug = f'{self.year}-{self.make}-{self.model}-review'
            else:
                base_slug = f'{self.make}-{self.model}-review'

            self.slug = slugify(base_slug)

        if not self.meta_title:
            self.meta_title = f'{self.title} | MyCarMarket Australia'

        if not self.meta_description:
            self.meta_description = self.summary[:300]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'review_detail',
            kwargs={'slug': self.slug}
        )

    def pros_list(self):
        return [
            item.strip()
            for item in self.pros.splitlines()
            if item.strip()
        ]

    def cons_list(self):
        return [
            item.strip()
            for item in self.cons.splitlines()
            if item.strip()
        ]


# ==========================================
# SECTION 01: CAR REVIEW MODEL
# END
# ==========================================