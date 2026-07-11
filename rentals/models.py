# ==========================================
# MyCarMarket Australia
# Version: v2.0.3
# File: rentals/models.py
# Description:
# Rental listings with maximum one compressed
# rental image and secure customer enquiries.
# Owner email and phone remain private.
# ==========================================


# ==========================================
# SECTION 1 START
# Imports
# ==========================================

import uuid

from io import BytesIO

from PIL import Image, ImageOps

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# ==========================================
# SECTION 1 END
# Imports
# ==========================================

# _____________________________________________


# ==========================================
# SECTION 2 START
# Rental Image Settings
# ==========================================

MAX_RENTAL_IMAGE_UPLOAD_SIZE = (
    10 * 1024 * 1024
)

MAX_RENTAL_IMAGE_WIDTH = 1600

MAX_RENTAL_IMAGE_HEIGHT = 1600

RENTAL_IMAGE_QUALITY = 82

# ==========================================
# SECTION 2 END
# Rental Image Settings
# ==========================================

# _____________________________________________


# ==========================================
# SECTION 3 START
# Rental Image Validation
# ==========================================

def validate_rental_image_size(
    image,
):

    if image.size > MAX_RENTAL_IMAGE_UPLOAD_SIZE:

        raise ValidationError(
            "The image must be 10 MB or smaller."
        )

# ==========================================
# SECTION 3 END
# Rental Image Validation
# ==========================================

# _____________________________________________


# ==========================================
# SECTION 4 START
# Rental Image Upload Path
# ==========================================

def rental_image_upload_path(
    instance,
    filename,
):

    unique_filename = (
        f"{uuid.uuid4().hex}.jpg"
    )

    rental_slug = (
        instance.rental.slug
        or "rental"
    )

    return (
        f"rentals/"
        f"{rental_slug}/"
        f"{unique_filename}"
    )

# ==========================================
# SECTION 4 END
# Rental Image Upload Path
# ==========================================

# _____________________________________________


# ==========================================
# SECTION 5 START
# Rental Image Compression
# ==========================================

def compress_rental_image(
    uploaded_image,
):

    uploaded_image.seek(0)

    try:

        image = Image.open(
            uploaded_image
        )

        image.load()

    except Exception as error:

        raise ValidationError(
            "The uploaded file is not a valid image."
        ) from error

    image = ImageOps.exif_transpose(
        image
    )

    if image.mode in (
        "RGBA",
        "LA",
    ):

        background = Image.new(
            "RGB",
            image.size,
            "white",
        )

        alpha_channel = (
            image.getchannel("A")
        )

        background.paste(
            image,
            mask=alpha_channel,
        )

        image = background

    elif image.mode == "P":

        image = image.convert(
            "RGBA"
        )

        background = Image.new(
            "RGB",
            image.size,
            "white",
        )

        alpha_channel = (
            image.getchannel("A")
        )

        background.paste(
            image,
            mask=alpha_channel,
        )

        image = background

    elif image.mode != "RGB":

        image = image.convert(
            "RGB"
        )

    image.thumbnail(
        (
            MAX_RENTAL_IMAGE_WIDTH,
            MAX_RENTAL_IMAGE_HEIGHT,
        ),
        Image.Resampling.LANCZOS,
    )

    output = BytesIO()

    image.save(
        output,
        format="JPEG",
        quality=RENTAL_IMAGE_QUALITY,
        optimize=True,
        progressive=True,
    )

    output.seek(0)

    compressed_filename = (
        f"{uuid.uuid4().hex}.jpg"
    )

    return ContentFile(
        output.read(),
        name=compressed_filename,
    )

# ==========================================
# SECTION 5 END
# Rental Image Compression
# ==========================================

# _____________________________________________


# ==========================================
# SECTION 6 START
# Rental Listing Model
# ==========================================

class RentalCar(models.Model):

    MODERATION_STATUS_CHOICES = [
        (
            "pending",
            "Pending",
        ),
        (
            "approved",
            "Approved",
        ),
        (
            "rejected",
            "Rejected",
        ),
    ]

    TRANSMISSION_CHOICES = [
        (
            "automatic",
            "Automatic",
        ),
        (
            "manual",
            "Manual",
        ),
    ]

    FUEL_TYPE_CHOICES = [
        (
            "petrol",
            "Petrol",
        ),
        (
            "diesel",
            "Diesel",
        ),
        (
            "hybrid",
            "Hybrid",
        ),
        (
            "electric",
            "Electric",
        ),
        (
            "lpg",
            "LPG",
        ),
        (
            "other",
            "Other",
        ),
    ]

    BODY_TYPE_CHOICES = [
        (
            "sedan",
            "Sedan",
        ),
        (
            "hatchback",
            "Hatchback",
        ),
        (
            "suv",
            "SUV",
        ),
        (
            "ute",
            "Ute",
        ),
        (
            "wagon",
            "Wagon",
        ),
        (
            "coupe",
            "Coupe",
        ),
        (
            "convertible",
            "Convertible",
        ),
        (
            "van",
            "Van",
        ),
        (
            "people_mover",
            "People Mover",
        ),
        (
            "other",
            "Other",
        ),
    ]

    STATE_CHOICES = [
        (
            "ACT",
            "Australian Capital Territory",
        ),
        (
            "NSW",
            "New South Wales",
        ),
        (
            "NT",
            "Northern Territory",
        ),
        (
            "QLD",
            "Queensland",
        ),
        (
            "SA",
            "South Australia",
        ),
        (
            "TAS",
            "Tasmania",
        ),
        (
            "VIC",
            "Victoria",
        ),
        (
            "WA",
            "Western Australia",
        ),
    ]

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rental_listings",
    )

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )

    make = models.CharField(
        max_length=100,
    )

    model = models.CharField(
        max_length=100,
    )

    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1900
            ),
        ],
    )

    body_type = models.CharField(
        max_length=30,
        choices=BODY_TYPE_CHOICES,
    )

    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPE_CHOICES,
    )

    seats = models.PositiveSmallIntegerField(
        default=5,
        validators=[
            MinValueValidator(
                1
            ),
        ],
    )

    colour = models.CharField(
        max_length=50,
        blank=True,
    )

    registration_number = models.CharField(
        max_length=20,
        blank=True,
    )

    daily_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                0
            ),
        ],
    )

    weekly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(
                0
            ),
        ],
    )

    security_deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(
                0
            ),
        ],
    )

    minimum_rental_days = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(
                1
            ),
        ],
    )

    unlimited_kilometres = models.BooleanField(
        default=False,
    )

    daily_kilometre_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    description = models.TextField()

    rental_conditions = models.TextField(
        blank=True,
    )

    pickup_address = models.CharField(
        max_length=255,
    )

    suburb = models.CharField(
        max_length=100,
    )

    state = models.CharField(
        max_length=3,
        choices=STATE_CHOICES,
    )

    postcode = models.CharField(
        max_length=4,
    )

    owner_name = models.CharField(
        max_length=150,
    )

    owner_email = models.EmailField()

    owner_phone = models.CharField(
        max_length=30,
    )

    available_from = models.DateField(
        null=True,
        blank=True,
    )

    available_until = models.DateField(
        null=True,
        blank=True,
    )

    is_available = models.BooleanField(
        default=True,
    )

    moderation_status = models.CharField(
        max_length=20,
        choices=MODERATION_STATUS_CHOICES,
        default="pending",
        db_index=True,
    )

    rejection_reason = models.TextField(
        blank=True,
    )

    is_approved = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    views = models.PositiveIntegerField(
        default=0,
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-is_featured",
            "-created_at",
        ]

        verbose_name = (
            "Rental Car"
        )

        verbose_name_plural = (
            "Rental Cars"
        )

        indexes = [
            models.Index(
                fields=[
                    "moderation_status",
                    "is_active",
                    "is_available",
                ],
            ),
            models.Index(
                fields=[
                    "state",
                    "suburb",
                ],
            ),
            models.Index(
                fields=[
                    "make",
                    "model",
                ],
            ),
        ]

    def __str__(self):

        return self.title

    def save(
        self,
        *args,
        **kwargs,
    ):

        if not self.title:

            self.title = (
                f"{self.year} "
                f"{self.make} "
                f"{self.model} "
                f"for Rent"
            )

        if not self.slug:

            base_slug = slugify(
                (
                    f"{self.year}-"
                    f"{self.make}-"
                    f"{self.model}-"
                    f"rental"
                )
            )

            slug = base_slug

            counter = 1

            while RentalCar.objects.filter(
                slug=slug
            ).exclude(
                pk=self.pk
            ).exists():

                slug = (
                    f"{base_slug}-"
                    f"{counter}"
                )

                counter += 1

            self.slug = slug

        if self.posted_by_id:

            if not self.owner_name:

                full_name = (
                    self.posted_by
                    .get_full_name()
                    .strip()
                )

                self.owner_name = (
                    full_name
                    or self.posted_by.username
                )

            if not self.owner_email:

                self.owner_email = (
                    self.posted_by.email
                )

        self.is_approved = (
            self.moderation_status
            == "approved"
        )

        super().save(
            *args,
            **kwargs,
        )

    def get_absolute_url(self):

        return reverse(
            "rental_detail",
            kwargs={
                "slug": self.slug,
            },
        )

    @property
    def primary_image(self):

        return self.images.first()

    @property
    def location(self):

        return (
            f"{self.suburb}, "
            f"{self.state}"
        )

# ==========================================
# SECTION 6 END
# Rental Listing Model
# ==========================================

# _____________________________________________


# ==========================================
# SECTION 7 START
# Rental Image Model
# Maximum One Image Per Rental
# ==========================================

class RentalCarImage(models.Model):

    rental = models.ForeignKey(
        RentalCar,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to=rental_image_upload_path,
        validators=[
            validate_rental_image_size,
        ],
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=True,
    )

    position = models.PositiveSmallIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "position",
            "created_at",
        ]

        verbose_name = (
            "Rental Car Image"
        )

        verbose_name_plural = (
            "Rental Car Images"
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "rental",
                ],
                name=(
                    "one_image_per_rental"
                ),
            ),
        ]

    def __str__(self):

        return (
            f"{self.rental.title} "
            f"- Image"
        )

    def clean(self):

        super().clean()

        if not self.image:

            raise ValidationError(
                {
                    "image": (
                        "Please upload one rental photo."
                    ),
                }
            )

        existing_image = (
            RentalCarImage.objects.filter(
                rental=self.rental,
            )
            .exclude(
                pk=self.pk,
            )
            .exists()
        )

        if existing_image:

            raise ValidationError(
                {
                    "image": (
                        "Only one photo is allowed "
                        "for each rental listing."
                    ),
                }
            )

    def save(
        self,
        *args,
        **kwargs,
    ):

        existing_image = (
            RentalCarImage.objects.filter(
                rental=self.rental,
            )
            .exclude(
                pk=self.pk,
            )
            .exists()
        )

        if existing_image:

            raise ValidationError(
                "Only one photo is allowed "
                "for each rental listing."
            )

        if not self.alt_text:

            self.alt_text = (
                self.rental.title
            )

        self.is_primary = True

        self.position = 0

        if (
            self.image
            and not self.image._committed
        ):

            self.image = compress_rental_image(
                self.image
            )

        super().save(
            *args,
            **kwargs,
        )

# ==========================================
# SECTION 7 END
# Rental Image Model
# ==========================================

# _____________________________________________


# ==========================================
# SECTION 8 START
# Rental Enquiry Model
# ==========================================

class RentalEnquiry(models.Model):

    STATUS_CHOICES = [
        (
            "new",
            "New",
        ),
        (
            "contacted",
            "Contacted",
        ),
        (
            "closed",
            "Closed",
        ),
        (
            "spam",
            "Spam",
        ),
    ]

    rental = models.ForeignKey(
        RentalCar,
        on_delete=models.CASCADE,
        related_name="enquiries",
    )

    customer_name = models.CharField(
        max_length=150,
    )

    customer_email = models.EmailField()

    customer_phone = models.CharField(
        max_length=30,
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        db_index=True,
    )

    owner_notified = models.BooleanField(
        default=False,
    )

    customer_ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

        verbose_name = (
            "Rental Enquiry"
        )

        verbose_name_plural = (
            "Rental Enquiries"
        )

        indexes = [
            models.Index(
                fields=[
                    "rental",
                    "status",
                    "created_at",
                ],
            ),
            models.Index(
                fields=[
                    "customer_email",
                    "created_at",
                ],
            ),
        ]

    def __str__(self):

        return (
            f"{self.customer_name} - "
            f"{self.rental.title}"
        )

# ==========================================
# SECTION 8 END
# Rental Enquiry Model
# ==========================================

# _____________________________________________