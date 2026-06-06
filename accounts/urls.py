# ==========================================
# MyCarMarket
# Version: v0.4.8
# File: accounts/urls.py
# Login + Logout Added
# ==========================================

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),

    path(
        'login/',
        LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
]