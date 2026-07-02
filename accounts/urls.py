# ==========================================
# MyCarMarket
# Version: v1.6.5
# File: accounts/urls.py
# Description: Register + Email Login + Email Verification
# ==========================================

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from accounts.forms import EmailAuthenticationForm
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),

    path(
        'verify-email-sent/',
        views.verify_email_sent,
        name='verify_email_sent'
    ),

    path(
        'verify-email/<uidb64>/<token>/',
        views.verify_email,
        name='verify_email'
    ),

    path(
        'login/',
        LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=EmailAuthenticationForm
        ),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
]