# ==========================================
# MyCarMarket Australia
# Version: v2.1.0
# File: rentals/forms.py
# Description:
# Rental listing creation form.
# Secure rental enquiry form.
# ==========================================

from django import forms

from rentals.models import RentalCar


# ==========================================
# SECTION 1 START
# Rental Car Listing Form
# ==========================================

class RentalCarForm(forms.ModelForm):

    rental_images = forms.ImageField(
        required=False,
        label="Vehicle Image",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "rental-form-file",
                "accept": "image/*",
            }
        ),
    )

    class Meta:

        model = RentalCar

        exclude = [
            "posted_by",
            "title",
            "slug",
            "views",
            "moderation_status",
            "rejection_reason",
            "is_approved",
            "is_active",
            "is_featured",
            "created_at",
            "updated_at",
        ]

        widgets = {

            "make": forms.TextInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Example: Toyota",
                }
            ),

            "model": forms.TextInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Example: Corolla",
                }
            ),

            "year": forms.NumberInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Example: 2022",
                    "min": "1900",
                    "max": "2030",
                }
            ),

            "body_type": forms.Select(
                attrs={
                    "class": "rental-form-select",
                }
            ),

            "transmission": forms.Select(
                attrs={
                    "class": "rental-form-select",
                }
            ),

            "fuel_type": forms.Select(
                attrs={
                    "class": "rental-form-select",
                }
            ),

            "seats": forms.NumberInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Example: 5",
                    "min": "1",
                }
            ),

            "doors": forms.NumberInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Example: 4",
                    "min": "1",
                }
            ),

            "colour": forms.TextInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Example: White",
                }
            ),

            "registration_number": forms.TextInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Vehicle registration",
                }
            ),

            "daily_price": forms.NumberInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Daily rental price",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "weekly_price": forms.NumberInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Optional weekly price",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "security_deposit": forms.NumberInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Security deposit",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "minimum_rental_days": forms.NumberInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Minimum rental days",
                    "min": "1",
                }
            ),

            "kilometres_included": forms.NumberInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Kilometres included per day",
                    "min": "0",
                }
            ),

            "extra_kilometre_cost": forms.NumberInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Extra kilometre cost",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "state": forms.Select(
                attrs={
                    "class": "rental-form-select",
                }
            ),

            "suburb": forms.TextInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Pickup suburb",
                }
            ),

            "postcode": forms.TextInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Postcode",
                    "inputmode": "numeric",
                    "maxlength": "4",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "rental-form-textarea",
                    "placeholder": (
                        "Describe the vehicle, rental conditions "
                        "and any important information."
                    ),
                    "rows": 7,
                }
            ),

            "rental_conditions": forms.Textarea(
                attrs={
                    "class": "rental-form-textarea",
                    "placeholder": (
                        "Add licence, age, deposit or pickup "
                        "requirements."
                    ),
                    "rows": 6,
                }
            ),

            "owner_name": forms.TextInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Your full name",
                    "autocomplete": "name",
                }
            ),

            "owner_email": forms.EmailInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Your email address",
                    "autocomplete": "email",
                }
            ),

            "owner_phone": forms.TextInput(
                attrs={
                    "class": "rental-form-input",
                    "placeholder": "Your phone number",
                    "autocomplete": "tel",
                }
            ),

            "is_available": forms.CheckboxInput(
                attrs={
                    "class": "rental-form-checkbox",
                }
            ),
        }

    def __init__(
        self,
        *args,
        user=None,
        **kwargs,
    ):

        super().__init__(
            *args,
            **kwargs,
        )

        self.user = user

        for field_name, field in self.fields.items():

            existing_class = field.widget.attrs.get(
                "class",
                "",
            )

            if isinstance(
                field.widget,
                forms.CheckboxInput,
            ):

                default_class = (
                    "rental-form-checkbox"
                )

            elif isinstance(
                field.widget,
                forms.Select,
            ):

                default_class = (
                    "rental-form-select"
                )

            elif isinstance(
                field.widget,
                forms.Textarea,
            ):

                default_class = (
                    "rental-form-textarea"
                )

            elif isinstance(
                field.widget,
                forms.ClearableFileInput,
            ):

                default_class = (
                    "rental-form-file"
                )

            else:

                default_class = (
                    "rental-form-input"
                )

            if default_class not in existing_class:

                field.widget.attrs[
                    "class"
                ] = (
                    f"{existing_class} "
                    f"{default_class}"
                ).strip()

        if user and user.is_authenticated:

            if "owner_name" in self.fields:

                full_name = user.get_full_name().strip()

                if full_name:

                    self.fields[
                        "owner_name"
                    ].initial = full_name

            if (
                "owner_email" in self.fields
                and user.email
            ):

                self.fields[
                    "owner_email"
                ].initial = user.email

    def clean_postcode(self):

        postcode = self.cleaned_data.get(
            "postcode",
        )

        if postcode is None:
            return postcode

        postcode = str(
            postcode
        ).strip()

        if postcode and (
            not postcode.isdigit()
            or len(postcode) != 4
        ):

            raise forms.ValidationError(
                "Enter a valid 4-digit Australian postcode."
            )

        return postcode

    def clean_owner_phone(self):

        phone = self.cleaned_data.get(
            "owner_phone",
            "",
        )

        if not phone:
            return phone

        phone = phone.strip()

        allowed_characters = set(
            "0123456789+()- "
        )

        if any(
            character not in allowed_characters
            for character in phone
        ):

            raise forms.ValidationError(
                "Enter a valid phone number."
            )

        number_count = sum(
            character.isdigit()
            for character in phone
        )

        if number_count < 8:

            raise forms.ValidationError(
                "Enter a valid phone number."
            )

        return phone


# ==========================================
# SECTION 1 END
# Rental Car Listing Form
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 2 START
# Rental Enquiry Form
# ==========================================

class RentalEnquiryForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        label="Your Name",
        widget=forms.TextInput(
            attrs={
                "class": "rental-form-input",
                "placeholder": "Enter your full name",
                "autocomplete": "name",
            }
        ),
    )

    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(
            attrs={
                "class": "rental-form-input",
                "placeholder": "Enter your email address",
                "autocomplete": "email",
            }
        ),
    )

    phone = forms.CharField(
        max_length=30,
        label="Your Phone Number",
        widget=forms.TextInput(
            attrs={
                "class": "rental-form-input",
                "placeholder": "Enter your phone number",
                "autocomplete": "tel",
            }
        ),
    )

    message = forms.CharField(
        max_length=2000,
        label="Message",
        widget=forms.Textarea(
            attrs={
                "class": "rental-form-textarea",
                "placeholder": (
                    "Ask about availability, pickup location "
                    "or rental conditions"
                ),
                "rows": 5,
            }
        ),
    )

    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

    def clean_phone(self):

        phone = self.cleaned_data[
            "phone"
        ].strip()

        allowed_characters = set(
            "0123456789+()- "
        )

        if any(
            character not in allowed_characters
            for character in phone
        ):

            raise forms.ValidationError(
                "Enter a valid phone number."
            )

        number_count = sum(
            character.isdigit()
            for character in phone
        )

        if number_count < 8:

            raise forms.ValidationError(
                "Enter a valid phone number."
            )

        return phone

    def clean_website(self):

        website = self.cleaned_data.get(
            "website",
            "",
        )

        if website:

            raise forms.ValidationError(
                "Invalid submission."
            )

        return website


# ==========================================
# SECTION 2 END
# Rental Enquiry Form
# ==========================================