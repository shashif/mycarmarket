# ==========================================
# MyCarMarket
# Version: v1.5.4
# File: vehicles/forms/car_form.py
# Description: Car Form + Smart Price Suggestion Ready Fields
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
            'kilometres',
            'body_type',
            'transmission',
            'fuel_type',
            'state',
            'suburb',
            'description',
            'price',
            'seller_name',
            'seller_email',
            'seller_phone',
            'is_active',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 2022 Toyota Camry Hybrid'
            }),

            'make': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_make',
                'placeholder': 'Example: Toyota'
            }),

            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_model',
                'placeholder': 'Example: Camry'
            }),

            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_year',
                'placeholder': 'Example: 2022'
            }),

            'kilometres': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_kilometres',
                'placeholder': 'Example: 45000'
            }),

            'body_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_body_type'
            }),

            'transmission': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_transmission'
            }),

            'fuel_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_fuel_type'
            }),

            'state': forms.Select(attrs={
                'class': 'form-control'
            }),

            'suburb': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter suburb or city'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'id_description',
                'rows': 5,
                'placeholder': (
                    'Describe the vehicle condition, service history, '
                    'registration, features and reason for selling.'
                )
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_price',
                'placeholder': 'Enter asking price'
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

            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }