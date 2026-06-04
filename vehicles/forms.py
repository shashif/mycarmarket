# ==========================================
# MyCarMarket
# Version: v0.3.2 - Buyer Enquiry Form
# File: vehicles/forms.py
# ==========================================

from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Your phone number',
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Hi, I am interested in this car. Is it still available?',
                'class': 'form-control',
                'rows': 5,
            }),
        }