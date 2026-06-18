# ==========================================
# MyCarMarket
# Version: v1.2.3
# File: vehicles/views/enquiry_views.py
# Dealer Enquiries Page
# ==========================================

from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from vehicles.models import Enquiry


@login_required
def dealer_enquiries(request):

    enquiries = Enquiry.objects.filter(

        dealer=request.user

    )

    unread_count = enquiries.filter(

        is_read=False

    ).count()

    return render(

        request,

        'vehicles/dealer_enquiries.html',

        {

            'enquiries': enquiries,

            'unread_count': unread_count,

        }

    )


# ==========================================
# END FILE
# ==========================================