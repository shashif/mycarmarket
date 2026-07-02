# ==========================================
# MyCarMarket
# Version: v1.6.3
# File: accounts/views.py
# Description: Email Based User Registration
# ==========================================

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from accounts.forms import EmailUserCreationForm


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, 'Account created successfully.')
            return redirect('car_list')

    else:
        form = EmailUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})