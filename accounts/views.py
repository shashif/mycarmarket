# ==========================================
# MyCarMarket
# Version: v1.6.5
# File: accounts/views.py
# Description: Email Registration With Verification
# ==========================================

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes

from accounts.forms import EmailUserCreationForm
from accounts.tokens import email_verification_token


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = email_verification_token.make_token(user)

            verification_url = request.build_absolute_uri(
                reverse(
                    'verify_email',
                    kwargs={
                        'uidb64': uid,
                        'token': token
                    }
                )
            )

            subject = 'Verify your MyCarMarket account'
            message = f"""
Hi,

Thank you for registering with MyCarMarket Australia.

Please verify your email address by clicking the link below:

{verification_url}

If you did not create this account, you can ignore this email.

Thanks,
MyCarMarket Australia
"""

            send_mail(
                subject,
                message,
                None,
                [user.email],
                fail_silently=False
            )

            return redirect('verify_email_sent')

    else:
        form = EmailUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_email_sent(request):
    return render(request, 'accounts/verify_email_sent.html')


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception:
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Your email has been verified. You can now log in.')
        return render(request, 'accounts/verify_email_success.html')

    return render(request, 'accounts/verify_email_invalid.html')