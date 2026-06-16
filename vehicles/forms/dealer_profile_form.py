# ==========================================
# MyCarMarket
# Version: v1.1.9
# File: vehicles/forms/dealer_profile_form.py
# Dealer Profile Edit Form + Cover Photo Position
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
                    'placeholder': 'Business Phone',
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
        }


# ==========================================
# END DEALER PROFILE FORM
# ==========================================