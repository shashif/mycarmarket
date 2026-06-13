# ==========================================
# MyCarMarket
# Version: v0.9.5
# File: vehicles/forms/enquiry_form.py
# Enquiry Form
# ==========================================

from django import forms
from vehicles.models import Enquiry


class EnquiryForm(forms.ModelForm):

    class Meta:
        model = Enquiry

        fields = [
            'name',
            'email',
            'phone',
            'message',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),

            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6
            }),
        }