# ==========================================
# MyCarMarket Australia
# Version: v2.2.12
# File: services/models.py
# Description:
# Car-related service marketplace with:
# - Service provider listings
# - Maximum one compressed image
# - Admin moderation
# - Secure customer enquiries
# - Private provider email and phone
# - Expanded to 25 automotive service categories
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

# ---------------------------------------------


# ==========================================
# SECTION 2 START
# Service Image Settings
# ==========================================

MAX_SERVICE_IMAGE_UPLOAD_SIZE = (
    10 * 1024 * 1024
)

MAX_SERVICE_IMAGE_WIDTH = 1600

MAX_SERVICE_IMAGE_HEIGHT = 1600

SERVICE_IMAGE_QUALITY = 82

# ==========================================
# SECTION 2 END
# Service Image Settings
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 3 START
# Service Image Validation
# ==========================================

def validate_service_image_size(
    image,
):

    if image.size > MAX_SERVICE_IMAGE_UPLOAD_SIZE:

        raise ValidationError(
            "The image must be 10 MB or smaller."
        )


# ==========================================
# SECTION 3 END
# Service Image Validation
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 4 START
# Service Image Upload Path
# ==========================================

def service_image_upload_path(
    instance,
    filename,
):

    unique_filename = (
        f"{uuid.uuid4().hex}.jpg"
    )

    service_slug = (
        instance.service.slug
        or "service"
    )

    return (
        f"services/"
        f"{service_slug}/"
        f"{unique_filename}"
    )


# ==========================================
# SECTION 4 END
# Service Image Upload Path
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 5 START
# Service Image Compression
# ==========================================

def compress_service_image(
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

        alpha_channel = image.getchannel(
            "A"
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

        alpha_channel = image.getchannel(
            "A"
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
            MAX_SERVICE_IMAGE_WIDTH,
            MAX_SERVICE_IMAGE_HEIGHT,
        ),
        Image.Resampling.LANCZOS,
    )

    output = BytesIO()

    image.save(
        output,
        format="JPEG",
        quality=SERVICE_IMAGE_QUALITY,
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
# Service Image Compression
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 6 START
# Car Service Model
# ==========================================

class CarService(models.Model):

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

    CATEGORY_CHOICES = [
        ("car_service", "Car Service"),
        ("logbook_servicing", "Logbook Servicing"),
        ("mechanic", "Mechanic"),
        ("car_detailing", "Car Detailing"),
        ("car_wash", "Car Wash"),
        ("tyres_wheels", "Tyres & Wheels"),
        ("battery_service", "Battery Service"),
        ("auto_electrician", "Auto Electrician"),
        ("roadworthy_inspection", "Roadworthy Inspection"),
        ("car_inspection", "Car Inspection"),
        ("towing", "Towing"),
        ("panel_beating_paint", "Panel Beating & Paint"),
        ("windscreen_repair", "Windscreen Repair"),
        ("headlight_restoration", "Headlight Restoration"),
        ("window_tinting", "Window Tinting"),
        ("air_conditioning_service", "Air Conditioning Service"),
        ("brake_clutch_repairs", "Brake & Clutch Repairs"),
        ("suspension_steering", "Suspension & Steering"),
        ("car_audio_multimedia", "Car Audio & Multimedia"),
        ("dash_cam_installation", "Dash Cam Installation"),
        ("accessories_installation", "Car Accessories Installation"),
        ("vehicle_transport", "Vehicle Transport"),
        ("driving_lessons", "Driving Lessons"),
        ("ev_service", "EV (Electric Vehicle) Service"),
        ("other", "Other Car Services"),
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
        related_name="car_service_listings",
    )

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )

    business_name = models.CharField(
        max_length=200,
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        db_index=True,
    )

    description = models.TextField()

    state = models.CharField(
        max_length=3,
        choices=STATE_CHOICES,
        db_index=True,
    )

    suburb = models.CharField(
        max_length=100,
        db_index=True,
    )

    postcode = models.CharField(
        max_length=4,
    )

    service_area = models.CharField(
        max_length=255,
        blank=True,
    )

    mobile_service = models.BooleanField(
        default=False,
        db_index=True,
    )

    starting_price = models.DecimalField(
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

    website = models.URLField(
        blank=True,
    )

    provider_name = models.CharField(
        max_length=150,
    )

    provider_email = models.EmailField()

    provider_phone = models.CharField(
        max_length=30,
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
            "Car Service"
        )

        verbose_name_plural = (
            "Car Services"
        )

        indexes = [
            models.Index(
                fields=[
                    "moderation_status",
                    "is_active",
                ],
            ),
            models.Index(
                fields=[
                    "category",
                    "state",
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
                    "mobile_service",
                    "is_active",
                ],
            ),
        ]

    def __str__(self):

        return (
            f"{self.title} - "
            f"{self.business_name}"
        )

    def save(
        self,
        *args,
        **kwargs,
    ):

        if not self.title:

            self.title = (
                f"{self.get_category_display()} "
                f"by {self.business_name}"
            )

        if not self.slug:

            base_slug = slugify(
                (
                    f"{self.business_name}-"
                    f"{self.title}-"
                    f"{self.suburb}"
                )
            )

            slug = base_slug

            counter = 1

            while CarService.objects.filter(
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

            if not self.provider_name:

                full_name = (
                    self.posted_by
                    .get_full_name()
                    .strip()
                )

                self.provider_name = (
                    full_name
                    or self.posted_by.username
                )

            if not self.provider_email:

                self.provider_email = (
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
            "service_detail",
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

    @property
    def display_price(self):

        if self.starting_price is None:

            return "Contact for price"

        return (
            f"From ${self.starting_price:,.2f}"
        )


# ==========================================
# SECTION 6 END
# Car Service Model
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 7 START
# Service Image Model
# Maximum One Image Per Listing
# ==========================================

class CarServiceImage(models.Model):

    service = models.ForeignKey(
        CarService,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to=service_image_upload_path,
        validators=[
            validate_service_image_size,
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
            "Car Service Image"
        )

        verbose_name_plural = (
            "Car Service Images"
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "service",
                ],
                name=(
                    "one_image_per_car_service"
                ),
            ),
        ]

    def __str__(self):

        return (
            f"{self.service.title} "
            f"- Image"
        )

    def clean(self):

        super().clean()

        if not self.image:

            raise ValidationError(
                {
                    "image": (
                        "Please upload one service image."
                    ),
                }
            )

        existing_image = (
            CarServiceImage.objects.filter(
                service=self.service,
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
                        "Only one image is allowed "
                        "for each service listing."
                    ),
                }
            )

    def save(
        self,
        *args,
        **kwargs,
    ):

        existing_image = (
            CarServiceImage.objects.filter(
                service=self.service,
            )
            .exclude(
                pk=self.pk,
            )
            .exists()
        )

        if existing_image:

            raise ValidationError(
                "Only one image is allowed "
                "for each service listing."
            )

        if not self.alt_text:

            self.alt_text = (
                self.service.title
            )

        self.is_primary = True

        self.position = 0

        if (
            self.image
            and not self.image._committed
        ):

            self.image = compress_service_image(
                self.image
            )

        super().save(
            *args,
            **kwargs,
        )


# ==========================================
# SECTION 7 END
# Service Image Model
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 8 START
# Service Enquiry Model
# ==========================================

class ServiceEnquiry(models.Model):

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

    service = models.ForeignKey(
        CarService,
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

    provider_notified = models.BooleanField(
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
            "Service Enquiry"
        )

        verbose_name_plural = (
            "Service Enquiries"
        )

        indexes = [
            models.Index(
                fields=[
                    "service",
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
            f"{self.service.title}"
        )


# ==========================================
# SECTION 8 END
# Service Enquiry Model
# ==========================================