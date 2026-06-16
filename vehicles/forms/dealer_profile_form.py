# ==========================================
# MyCarMarket
# Version: v1.2.1
# File: vehicles/forms/dealer_profile_form.py
# Full Dealer Profile Edit Form + Dropdown Opening Hours
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


class DealerProfileForm(forms.ModelForm):

    monday_open_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    monday_close_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    tuesday_open_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    tuesday_close_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    wednesday_open_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    wednesday_close_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    thursday_open_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    thursday_close_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    friday_open_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    friday_close_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    saturday_open_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    saturday_close_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    sunday_open_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    sunday_close_time = forms.TimeField(
        required=False,
        widget=forms.Select(
            choices=TIME_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

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

            'monday_closed': forms.CheckboxInput(),
            'tuesday_closed': forms.CheckboxInput(),
            'wednesday_closed': forms.CheckboxInput(),
            'thursday_closed': forms.CheckboxInput(),
            'friday_closed': forms.CheckboxInput(),
            'saturday_closed': forms.CheckboxInput(),
            'sunday_closed': forms.CheckboxInput(),

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