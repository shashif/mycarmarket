# ==========================================
# MyCarMarket Australia
# Version: v2.2.0
# File: services/forms.py
# Description:
# Car Services forms with:
# - Public service listing form
# - Maximum one service image
# - Secure customer enquiry form
# - Australian postcode validation
# - Provider contact validation
# - Consistent MyCarMarket form styling
# ==========================================


# ==========================================
# SECTION 1 START
# Imports
# ==========================================

import re

from django import forms
from django.core.exceptions import ValidationError

from services.models import (
    CarService,
    CarServiceImage,
    ServiceEnquiry,
)

# ==========================================
# SECTION 1 END
# Imports
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 2 START
# Shared Form Styling
# ==========================================

TEXT_INPUT_CLASS = (
    "service-form-control"
)

SELECT_INPUT_CLASS = (
    "service-form-control "
    "service-form-select"
)

TEXTAREA_INPUT_CLASS = (
    "service-form-control "
    "service-form-textarea"
)

CHECKBOX_INPUT_CLASS = (
    "service-form-checkbox"
)

FILE_INPUT_CLASS = (
    "service-form-control "
    "service-form-file"
)

# ==========================================
# SECTION 2 END
# Shared Form Styling
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 3 START
# Car Service Listing Form
# ==========================================

class CarServiceForm(forms.ModelForm):

    service_image = forms.ImageField(
        required=True,
        label="Service Image",
        help_text=(
            "Upload one clear image representing "
            "your service or business. Maximum 10 MB."
        ),
        widget=forms.ClearableFileInput(
            attrs={
                "class": FILE_INPUT_CLASS,
                "accept": (
                    "image/jpeg,"
                    "image/jpg,"
                    "image/png,"
                    "image/webp"
                ),
            },
        ),
    )

    terms_confirmed = forms.BooleanField(
        required=True,
        label=(
            "I confirm that the information provided "
            "is accurate and I am authorised to list "
            "this service."
        ),
        widget=forms.CheckboxInput(
            attrs={
                "class": CHECKBOX_INPUT_CLASS,
            },
        ),
    )

    class Meta:

        model = CarService

        fields = [
            "title",
            "business_name",
            "category",
            "description",
            "state",
            "suburb",
            "postcode",
            "service_area",
            "mobile_service",
            "starting_price",
            "website",
            "provider_name",
            "provider_email",
            "provider_phone",
        ]

        labels = {
            "title": "Service Listing Title",
            "business_name": "Business Name",
            "category": "Service Category",
            "description": "Service Description",
            "state": "State or Territory",
            "suburb": "Suburb",
            "postcode": "Postcode",
            "service_area": "Service Area",
            "mobile_service": (
                "This is a mobile service"
            ),
            "starting_price": "Starting Price",
            "website": "Business Website",
            "provider_name": "Contact Person",
            "provider_email": "Contact Email",
            "provider_phone": "Contact Phone",
        }

        help_texts = {
            "title": (
                "Use a clear title describing the "
                "service you provide."
            ),
            "business_name": (
                "Enter your registered or trading "
                "business name."
            ),
            "description": (
                "Describe the services offered, "
                "experience, inclusions and any "
                "important conditions."
            ),
            "service_area": (
                "Optional. Example: Melbourne CBD "
                "and surrounding suburbs."
            ),
            "mobile_service": (
                "Select this if you travel to the "
                "customer's location."
            ),
            "starting_price": (
                "Optional. Enter the minimum service "
                "price in Australian dollars."
            ),
            "website": (
                "Optional. Include the full URL, "
                "for example https://example.com.au."
            ),
            "provider_email": (
                "Your email will remain private and "
                "will not be displayed publicly."
            ),
            "provider_phone": (
                "Your phone number will remain private "
                "and will not be displayed publicly."
            ),
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "Example: Mobile Car Detailing "
                        "in Melbourne"
                    ),
                    "maxlength": "200",
                },
            ),
            "business_name": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "Enter your business name"
                    ),
                    "maxlength": "200",
                },
            ),
            "category": forms.Select(
                attrs={
                    "class": SELECT_INPUT_CLASS,
                },
            ),
            "description": forms.Textarea(
                attrs={
                    "class": TEXTAREA_INPUT_CLASS,
                    "placeholder": (
                        "Describe your service, "
                        "experience, inclusions and "
                        "service conditions..."
                    ),
                    "rows": "8",
                },
            ),
            "state": forms.Select(
                attrs={
                    "class": SELECT_INPUT_CLASS,
                },
            ),
            "suburb": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "Enter suburb",
                    "maxlength": "100",
                },
            ),
            "postcode": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "Example: 3000"
                    ),
                    "maxlength": "4",
                    "inputmode": "numeric",
                    "pattern": "[0-9]{4}",
                },
            ),
            "service_area": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "Example: Melbourne CBD and "
                        "western suburbs"
                    ),
                    "maxlength": "255",
                },
            ),
            "mobile_service": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_INPUT_CLASS,
                },
            ),
            "starting_price": forms.NumberInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": "0.00",
                    "min": "0",
                    "step": "0.01",
                    "inputmode": "decimal",
                },
            ),
            "website": forms.URLInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "https://example.com.au"
                    ),
                },
            ),
            "provider_name": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "Enter contact person's name"
                    ),
                    "maxlength": "150",
                    "autocomplete": "name",
                },
            ),
            "provider_email": forms.EmailInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "Enter contact email"
                    ),
                    "autocomplete": "email",
                },
            ),
            "provider_phone": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "Example: 0412 345 678"
                    ),
                    "maxlength": "30",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                },
            ),
        }

    def __init__(
        self,
        *args,
        **kwargs,
    ):

        self.request = kwargs.pop(
            "request",
            None,
        )

        super().__init__(
            *args,
            **kwargs,
        )

        self.fields[
            "category"
        ].empty_label = (
            "Select a service category"
        )

        self.fields[
            "state"
        ].empty_label = (
            "Select a state or territory"
        )

        if (
            self.instance
            and self.instance.pk
            and self.instance.images.exists()
        ):

            self.fields[
                "service_image"
            ].required = False

            self.fields[
                "service_image"
            ].help_text = (
                "Leave this blank to keep the existing "
                "image, or upload a new image to replace it."
            )

    def clean_title(
        self,
    ):

        title = (
            self.cleaned_data
            .get(
                "title",
                "",
            )
            .strip()
        )

        if len(title) < 5:

            raise ValidationError(
                "Please enter a more descriptive "
                "service listing title."
            )

        return title

    def clean_business_name(
        self,
    ):

        business_name = (
            self.cleaned_data
            .get(
                "business_name",
                "",
            )
            .strip()
        )

        if len(business_name) < 2:

            raise ValidationError(
                "Please enter a valid business name."
            )

        return business_name

    def clean_description(
        self,
    ):

        description = (
            self.cleaned_data
            .get(
                "description",
                "",
            )
            .strip()
        )

        if len(description) < 50:

            raise ValidationError(
                "Please provide at least 50 characters "
                "describing your service."
            )

        return description

    def clean_suburb(
        self,
    ):

        suburb = (
            self.cleaned_data
            .get(
                "suburb",
                "",
            )
            .strip()
        )

        if len(suburb) < 2:

            raise ValidationError(
                "Please enter a valid suburb."
            )

        if not re.fullmatch(
            r"[A-Za-zÀ-ÖØ-öø-ÿ' .-]+",
            suburb,
        ):

            raise ValidationError(
                "The suburb may only contain letters, "
                "spaces, apostrophes and hyphens."
            )

        return " ".join(
            word.capitalize()
            for word in suburb.split()
        )

    def clean_postcode(
        self,
    ):

        postcode = (
            self.cleaned_data
            .get(
                "postcode",
                "",
            )
            .strip()
        )

        if not re.fullmatch(
            r"\d{4}",
            postcode,
        ):

            raise ValidationError(
                "Please enter a valid four-digit "
                "Australian postcode."
            )

        return postcode

    def clean_service_area(
        self,
    ):

        service_area = (
            self.cleaned_data
            .get(
                "service_area",
                "",
            )
            .strip()
        )

        return service_area

    def clean_starting_price(
        self,
    ):

        starting_price = (
            self.cleaned_data
            .get(
                "starting_price"
            )
        )

        if (
            starting_price is not None
            and starting_price < 0
        ):

            raise ValidationError(
                "Starting price cannot be negative."
            )

        return starting_price

    def clean_website(
        self,
    ):

        website = (
            self.cleaned_data
            .get(
                "website",
                "",
            )
            .strip()
        )

        return website

    def clean_provider_name(
        self,
    ):

        provider_name = (
            self.cleaned_data
            .get(
                "provider_name",
                "",
            )
            .strip()
        )

        if len(provider_name) < 2:

            raise ValidationError(
                "Please enter a valid contact name."
            )

        return provider_name

    def clean_provider_email(
        self,
    ):

        provider_email = (
            self.cleaned_data
            .get(
                "provider_email",
                "",
            )
            .strip()
            .lower()
        )

        return provider_email

    def clean_provider_phone(
        self,
    ):

        provider_phone = (
            self.cleaned_data
            .get(
                "provider_phone",
                "",
            )
            .strip()
        )

        normalised_phone = re.sub(
            r"[\s()+.-]",
            "",
            provider_phone,
        )

        if not normalised_phone.isdigit():

            raise ValidationError(
                "Please enter a valid phone number."
            )

        if not 8 <= len(
            normalised_phone
        ) <= 15:

            raise ValidationError(
                "Please enter a valid phone number "
                "between 8 and 15 digits."
            )

        return provider_phone

    def clean_service_image(
        self,
    ):

        service_image = (
            self.cleaned_data
            .get(
                "service_image"
            )
        )

        if not service_image:

            if (
                self.instance
                and self.instance.pk
                and self.instance.images.exists()
            ):

                return None

            raise ValidationError(
                "Please upload one service image."
            )

        allowed_content_types = [
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/webp",
        ]

        content_type = getattr(
            service_image,
            "content_type",
            "",
        )

        if (
            content_type
            and content_type
            not in allowed_content_types
        ):

            raise ValidationError(
                "Please upload a JPG, PNG or WebP image."
            )

        return service_image

    def save(
        self,
        commit=True,
    ):

        service = super().save(
            commit=False,
        )

        if (
            self.request
            and self.request.user.is_authenticated
        ):

            service.posted_by = (
                self.request.user
            )

        service.moderation_status = (
            "pending"
        )

        service.is_approved = False

        service.approved_at = None

        service.rejection_reason = ""

        if commit:

            service.save()

            service_image = (
                self.cleaned_data
                .get(
                    "service_image"
                )
            )

            if service_image:

                CarServiceImage.objects.filter(
                    service=service,
                ).delete()

                CarServiceImage.objects.create(
                    service=service,
                    image=service_image,
                    alt_text=service.title,
                    is_primary=True,
                    position=0,
                )

        return service


# ==========================================
# SECTION 3 END
# Car Service Listing Form
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 4 START
# Service Enquiry Form
# ==========================================

class ServiceEnquiryForm(forms.ModelForm):

    website = forms.CharField(
        required=False,
        label="Website",
        widget=forms.TextInput(
            attrs={
                "class": (
                    "service-honeypot-field"
                ),
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
            },
        ),
    )

    class Meta:

        model = ServiceEnquiry

        fields = [
            "customer_name",
            "customer_email",
            "customer_phone",
            "message",
        ]

        labels = {
            "customer_name": "Your Name",
            "customer_email": "Your Email",
            "customer_phone": "Your Phone",
            "message": "Your Message",
        }

        widgets = {
            "customer_name": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "Enter your full name"
                    ),
                    "maxlength": "150",
                    "autocomplete": "name",
                },
            ),
            "customer_email": forms.EmailInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "Enter your email address"
                    ),
                    "autocomplete": "email",
                },
            ),
            "customer_phone": forms.TextInput(
                attrs={
                    "class": TEXT_INPUT_CLASS,
                    "placeholder": (
                        "Example: 0412 345 678"
                    ),
                    "maxlength": "30",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                },
            ),
            "message": forms.Textarea(
                attrs={
                    "class": TEXTAREA_INPUT_CLASS,
                    "placeholder": (
                        "Describe the service you need, "
                        "your preferred date and any "
                        "important details..."
                    ),
                    "rows": "6",
                    "maxlength": "2000",
                },
            ),
        }

    def clean_customer_name(
        self,
    ):

        customer_name = (
            self.cleaned_data
            .get(
                "customer_name",
                "",
            )
            .strip()
        )

        if len(customer_name) < 2:

            raise ValidationError(
                "Please enter your full name."
            )

        return customer_name

    def clean_customer_email(
        self,
    ):

        customer_email = (
            self.cleaned_data
            .get(
                "customer_email",
                "",
            )
            .strip()
            .lower()
        )

        return customer_email

    def clean_customer_phone(
        self,
    ):

        customer_phone = (
            self.cleaned_data
            .get(
                "customer_phone",
                "",
            )
            .strip()
        )

        normalised_phone = re.sub(
            r"[\s()+.-]",
            "",
            customer_phone,
        )

        if not normalised_phone.isdigit():

            raise ValidationError(
                "Please enter a valid phone number."
            )

        if not 8 <= len(
            normalised_phone
        ) <= 15:

            raise ValidationError(
                "Please enter a valid phone number "
                "between 8 and 15 digits."
            )

        return customer_phone

    def clean_message(
        self,
    ):

        message = (
            self.cleaned_data
            .get(
                "message",
                "",
            )
            .strip()
        )

        if len(message) < 20:

            raise ValidationError(
                "Please provide at least 20 characters "
                "describing the service you need."
            )

        if len(message) > 2000:

            raise ValidationError(
                "Your message cannot exceed "
                "2,000 characters."
            )

        return message

    def clean_website(
        self,
    ):

        website = (
            self.cleaned_data
            .get(
                "website",
                "",
            )
            .strip()
        )

        if website:

            raise ValidationError(
                "Unable to submit this enquiry."
            )

        return website


# ==========================================
# SECTION 4 END
# Service Enquiry Form
# ==========================================