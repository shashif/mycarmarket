# ==========================================
# MyCarMarket
# Version: v1.2.2
# File: vehicles/forms/dealer_profile_form.py
# Full Dealer Profile Edit Form + Professional Dealer Fields
# ==========================================

from django import forms
from vehicles.models import DealerProfile


TIME_CHOICES = [
    ('', 'Select time'),
    ('07:00', '7:00 AM'),
    ('07:30', '7:30 AM'),
    ('08:00', '8:00 AM'),
    ('08:30', '8:30 AM'),
    ('09:00', '9:00 AM'),
    ('09:30', '9:30 AM'),
    ('10:00', '10:00 AM'),
    ('10:30', '10:30 AM'),
    ('11:00', '11:00 AM'),
    ('11:30', '11:30 AM'),
    ('12:00', '12:00 PM'),
    ('12:30', '12:30 PM'),
    ('13:00', '1:00 PM'),
    ('13:30', '1:30 PM'),
    ('14:00', '2:00 PM'),
    ('14:30', '2:30 PM'),
    ('15:00', '3:00 PM'),
    ('15:30', '3:30 PM'),
    ('16:00', '4:00 PM'),
    ('16:30', '4:30 PM'),
    ('17:00', '5:00 PM'),
    ('17:30', '5:30 PM'),
    ('18:00', '6:00 PM'),
    ('18:30', '6:30 PM'),
    ('19:00', '7:00 PM'),
    ('19:30', '7:30 PM'),
    ('20:00', '8:00 PM'),
]


def time_select_field():
    return forms.TimeField(
        required=False,
        input_formats=['%H:%M'],
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )


class DealerProfileForm(forms.ModelForm):

    monday_open_time = time_select_field()
    monday_close_time = time_select_field()

    tuesday_open_time = time_select_field()
    tuesday_close_time = time_select_field()

    wednesday_open_time = time_select_field()
    wednesday_close_time = time_select_field()

    thursday_open_time = time_select_field()
    thursday_close_time = time_select_field()

    friday_open_time = time_select_field()
    friday_close_time = time_select_field()

    saturday_open_time = time_select_field()
    saturday_close_time = time_select_field()

    sunday_open_time = time_select_field()
    sunday_close_time = time_select_field()

    class Meta:

        model = DealerProfile

        fields = [

            'business_name',
            'business_slogan',
            'business_description',

            'years_in_business',
            'dealer_owner_name',
            'dealer_owner_title',
            'dealer_owner_photo',
            'google_maps_link',

            'logo',
            'banner',
            'banner_position',

            'website',
            'business_phone',
            'business_email',
            'address',
            'abn',

            'open_24_hours',

            'monday_closed',
            'monday_open_time',
            'monday_close_time',

            'tuesday_closed',
            'tuesday_open_time',
            'tuesday_close_time',

            'wednesday_closed',
            'wednesday_open_time',
            'wednesday_close_time',

            'thursday_closed',
            'thursday_open_time',
            'thursday_close_time',

            'friday_closed',
            'friday_open_time',
            'friday_close_time',

            'saturday_closed',
            'saturday_open_time',
            'saturday_close_time',

            'sunday_closed',
            'sunday_open_time',
            'sunday_close_time',

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

            'business_slogan': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Quality used cars you can trust',
                }
            ),

            'business_description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Write about your dealership',
                }
            ),

            'years_in_business': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'placeholder': 'Example: 5',
                }
            ),

            'dealer_owner_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Owner / Manager Name',
                }
            ),

            'dealer_owner_title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Dealer Principal',
                }
            ),

            'dealer_owner_photo': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'google_maps_link': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Paste Google Maps business/profile link',
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

            'open_24_hours': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),

            'monday_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tuesday_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wednesday_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'thursday_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'friday_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'saturday_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sunday_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

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

            'show_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_phone': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'finance_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'trade_in_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'extended_warranty': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'delivery_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'test_drive_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ==========================================
# END DEALER PROFILE FORM
# ==========================================