# ==========================================
# MyCarMarket
# Version: v1.6.3
# File: accounts/urls.py
# Description: Register + Email Login + Logout
# ==========================================

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from accounts.forms import EmailAuthenticationForm
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),

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