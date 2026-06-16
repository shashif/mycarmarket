# ==========================================
# MyCarMarket
# Version: v1.1.8
# File: vehicles/views/dealer_profile_edit_views.py
# Dealer Profile Edit View
# ==========================================

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from vehicles.models import DealerProfile
from vehicles.forms import DealerProfileForm


@login_required
def edit_dealer_profile(request):

    dealer_profile, created = DealerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = DealerProfileForm(
            request.POST,
            request.FILES,
            instance=dealer_profile
        )

        if form.is_valid():

            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            messages.success(
                request,
                'Your dealer profile has been updated successfully.'
            )

            return redirect(
                'dealer_detail',
                username=request.user.username
            )

    else:

        form = DealerProfileForm(
            instance=dealer_profile
        )

    return render(
        request,
        'vehicles/dealer_profile_edit.html',
        {
            'form': form,
            'dealer_profile': dealer_profile,
        }
    )


# ==========================================
# END DEALER PROFILE EDIT VIEW
# ==========================================