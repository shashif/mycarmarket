# ==========================================
# MyCarMarket
# Version: v1.2.0
# File: vehicles/forms/dealer_profile_form.py
# Full Dealer Profile Edit Form + Google Style Opening Hours
# ==========================================

from django import forms

from vehicles.models import DealerProfile


class DealerProfileForm(forms.ModelForm):

    class Meta:

        model = DealerProfile

        fields = [

            'business_name',

            'business_description',

            'logo',

            'banner',

            'banner_position',

            'website',

            'business_phone',

            'business_email',

            'address',

            'abn',

            'open_24_hours',

            'monday_hours',

            'tuesday_hours',

            'wednesday_hours',

            'thursday_hours',

            'friday_hours',

            'saturday_hours',

            'sunday_hours',

            'facebook',

            'instagram',

            'tiktok',

            'youtube',

            'show_email',

            'show_phone',

            'finance_available',

            'trade_in_available',

            'extended_warranty',

            'delivery_available',

            'test_drive_available',
        ]

        widgets = {

            'business_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Business Name',
                }
            ),

            'business_description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Write about your dealership',
                }
            ),

            'logo': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'banner': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'banner_position': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'website': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://example.com',
                }
            ),

            'business_phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Dealer Phone Number',
                }
            ),

            'business_email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Business Email',
                }
            ),

            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Business Address',
                }
            ),

            'abn': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ABN',
                }
            ),

            'open_24_hours': forms.CheckboxInput(),

            'monday_hours': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '9:00 AM - 5:00 PM',
                }
            ),

            'tuesday_hours': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '9:00 AM - 5:00 PM',
                }
            ),

            'wednesday_hours': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '9:00 AM - 5:00 PM',
                }
            ),

            'thursday_hours': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '9:00 AM - 5:00 PM',
                }
            ),

            'friday_hours': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '9:00 AM - 5:00 PM',
                }
            ),

            'saturday_hours': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Closed',
                }
            ),

            'sunday_hours': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Closed',
                }
            ),

            'facebook': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Facebook URL',
                }
            ),

            'instagram': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Instagram URL',
                }
            ),

            'tiktok': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'TikTok URL',
                }
            ),

            'youtube': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'YouTube URL',
                }
            ),

            'show_email': forms.CheckboxInput(),

            'show_phone': forms.CheckboxInput(),

            'finance_available': forms.CheckboxInput(),

            'trade_in_available': forms.CheckboxInput(),

            'extended_warranty': forms.CheckboxInput(),

            'delivery_available': forms.CheckboxInput(),

            'test_drive_available': forms.CheckboxInput(),
        }


# ==========================================
# END DEALER PROFILE FORM
# ==========================================