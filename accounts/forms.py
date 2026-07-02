# ==========================================
# MyCarMarket
# Version: v1.6.3
# File: accounts/forms.py
# Description: Email Registration + Email Login Forms
# ==========================================

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email address",
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email",
            "autocomplete": "email",
        })
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email").lower().strip()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].lower().strip()

        user.username = email
        user.email = email

        if commit:
            user.save()

        return user


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={
            "autofocus": True,
            "placeholder": "Enter your email",
            "autocomplete": "email",
        })
    )

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email and password:
            email = email.lower().strip()

            try:
                user_obj = User.objects.get(email__iexact=email)
                username = user_obj.username
            except User.DoesNotExist:
                username = email

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError(
                    "Invalid email or password.",
                    code="invalid_login"
                )

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data