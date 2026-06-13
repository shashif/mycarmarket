# ==========================================
# MyCarMarket
# Version: v0.9.5
# File: vehicles/forms/car_form.py
# Car Form
# ==========================================

from django import forms
from vehicles.models import Car


class CarForm(forms.ModelForm):

    class Meta:
        model = Car

        fields = [
            'title',
            'make',
            'model',
            'year',
            'price',
            'kilometres',
            'body_type',
            'transmission',
            'fuel_type',
            'state',
            'suburb',
            'description',
            'seller_name',
            'seller_email',
            'seller_phone',
            'is_active',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'make': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'model': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'year': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'kilometres': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'body_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'transmission': forms.Select(attrs={
                'class': 'form-control'
            }),

            'fuel_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'state': forms.Select(attrs={
                'class': 'form-control'
            }),

            'suburb': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Suburb or City'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),

            'seller_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'seller_email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            'seller_phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }