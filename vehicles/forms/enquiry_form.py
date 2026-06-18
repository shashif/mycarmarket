# ==========================================
# MyCarMarket
# Version: v1.2.3
# File: vehicles/forms/enquiry_form.py
# Dealer Enquiry Form - Phone Required
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

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Name',
                    'required': 'required',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Email',
                    'required': 'required',
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Phone Number',
                    'required': 'required',
                }
            ),

            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Hi, I am interested in this vehicle. Is it still available?',
                    'required': 'required',
                }
            ),
        }

    def clean_phone(self):

        phone = self.cleaned_data.get('phone', '')

        phone = phone.strip()
        phone = phone.replace(' ', '')

        if len(phone) < 8:

            raise forms.ValidationError(
                'Please enter a valid phone number.'
            )

        return phone


# ==========================================
# END ENQUIRY FORM
# ==========================================