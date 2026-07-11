# ==========================================
# MyCarMarket Australia
# Version: v2.1.0
# File: rentals/views.py
# Description:
# Rental list, detail and create views.
# Secure rental enquiry email submission.
# Rental owner email remains private.
# ==========================================

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views.decorators.http import require_POST

from core.models import SiteSettings
from rentals.forms import (
    RentalCarForm,
    RentalEnquiryForm,
)
from rentals.models import (
    RentalCar,
    RentalCarImage,
)


# ==========================================
# SECTION 1 START
# Rental List
# ==========================================

def rental_list(request):

    rentals = RentalCar.objects.filter(
        is_active=True,
        is_available=True,
        moderation_status="approved",
        is_approved=True,
    ).order_by(
        "-is_featured",
        "-created_at",
    )

    search = request.GET.get(
        "search",
        "",
    ).strip()

    state = request.GET.get(
        "state",
        "",
    ).strip()

    body_type = request.GET.get(
        "body_type",
        "",
    ).strip()

    if search:

        rentals = rentals.filter(
            Q(make__icontains=search)
            | Q(model__icontains=search)
            | Q(title__icontains=search)
            | Q(suburb__icontains=search)
        )

    if state:

        rentals = rentals.filter(
            state=state,
        )

    if body_type:

        rentals = rentals.filter(
            body_type=body_type,
        )

    paginator = Paginator(
        rentals,
        12,
    )

    page_number = request.GET.get(
        "page",
    )

    page_obj = paginator.get_page(
        page_number,
    )

    context = {
        "page_obj": page_obj,
        "rentals": page_obj,
        "settings": SiteSettings.objects.first(),
        "search": search,
        "selected_state": state,
        "selected_body_type": body_type,
        "states": RentalCar.STATE_CHOICES,
        "body_types": RentalCar.BODY_TYPE_CHOICES,
    }

    return render(
        request,
        "rentals/rental_list.html",
        context,
    )


# ==========================================
# SECTION 1 END
# Rental List
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 2 START
# Rental Detail
# ==========================================

def rental_detail(
    request,
    slug,
):

    rental_queryset = RentalCar.objects.filter(
        slug=slug,
        is_active=True,
    )

    if request.user.is_authenticated:

        rental_queryset = rental_queryset.filter(
            Q(
                moderation_status="approved",
                is_approved=True,
            )
            | Q(
                posted_by=request.user,
            )
        )

    else:

        rental_queryset = rental_queryset.filter(
            moderation_status="approved",
            is_approved=True,
        )

    rental = get_object_or_404(
        rental_queryset,
    )

    if (
        rental.moderation_status == "approved"
        and rental.is_approved
    ):

        RentalCar.objects.filter(
            pk=rental.pk,
        ).update(
            views=F("views") + 1,
        )

        rental.refresh_from_db()

    related_rentals = RentalCar.objects.filter(
        moderation_status="approved",
        is_approved=True,
        is_active=True,
        is_available=True,
        make=rental.make,
    ).exclude(
        pk=rental.pk,
    ).order_by(
        "-is_featured",
        "-created_at",
    )[:8]

    enquiry_form = RentalEnquiryForm()

    context = {
        "rental": rental,
        "images": rental.images.all(),
        "related_rentals": related_rentals,
        "enquiry_form": enquiry_form,
        "settings": SiteSettings.objects.first(),
    }

    return render(
        request,
        "rentals/rental_detail.html",
        context,
    )


# ==========================================
# SECTION 2 END
# Rental Detail
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 3 START
# Create Rental Listing
# ==========================================

@login_required
def create_rental(request):

    if request.method == "POST":

        form = RentalCarForm(
            request.POST,
            request.FILES,
            user=request.user,
        )

        if form.is_valid():

            rental = form.save(
                commit=False,
            )

            rental.posted_by = request.user

            rental.title = (
                f"{rental.year} "
                f"{rental.make} "
                f"{rental.model} "
                f"for Rent"
            )

            rental.moderation_status = "pending"
            rental.is_active = True
            rental.is_approved = False

            rental.save()

            uploaded_image = request.FILES.get(
                "rental_images"
            )

            if uploaded_image:

                RentalCarImage.objects.create(
                    rental=rental,
                    image=uploaded_image,
                    is_primary=True,
                    position=1,
                )

            messages.success(
                request,
                (
                    "Your rental listing has been submitted "
                    "successfully and is waiting for admin approval."
                ),
            )

            return redirect(
                "rental_detail",
                slug=rental.slug,
            )

    else:

        form = RentalCarForm(
            user=request.user,
        )

    context = {
        "form": form,
        "settings": SiteSettings.objects.first(),
    }

    return render(
        request,
        "rentals/create_rental.html",
        context,
    )


# ==========================================
# SECTION 3 END
# Create Rental Listing
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 4 START
# Submit Rental Enquiry
# ==========================================

@require_POST
def submit_rental_enquiry(
    request,
    pk,
):

    rental = get_object_or_404(
        RentalCar,
        pk=pk,
        is_active=True,
        is_available=True,
        moderation_status="approved",
        is_approved=True,
    )

    form = RentalEnquiryForm(
        request.POST,
    )

    if not form.is_valid():

        for field_errors in form.errors.values():

            for error in field_errors:

                messages.error(
                    request,
                    str(error),
                )

        return redirect(
            "rental_detail",
            slug=rental.slug,
        )

    owner_email = (
        rental.owner_email or ""
    ).strip()

    if not owner_email:

        messages.error(
            request,
            (
                "The rental owner cannot receive "
                "enquiries at the moment."
            ),
        )

        return redirect(
            "rental_detail",
            slug=rental.slug,
        )

    customer_name = form.cleaned_data[
        "name"
    ]

    customer_email = form.cleaned_data[
        "email"
    ]

    customer_phone = form.cleaned_data[
        "phone"
    ]

    customer_message = form.cleaned_data[
        "message"
    ]

    vehicle_name = (
        f"{rental.year} "
        f"{rental.make} "
        f"{rental.model}"
    )

    email_subject = (
        f"New rental enquiry for {vehicle_name}"
    )

    email_body = f"""
Hello {rental.owner_name},

You have received a new rental enquiry through MyCarMarket Australia.

RENTAL VEHICLE
{vehicle_name}

CUSTOMER DETAILS

Name:
{customer_name}

Email:
{customer_email}

Phone:
{customer_phone}

CUSTOMER MESSAGE

{customer_message}

You can reply directly to this email to contact the customer.

This enquiry was submitted through MyCarMarket Australia.
"""

    email = EmailMessage(
        subject=email_subject,
        body=email_body.strip(),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[
            owner_email,
        ],
        reply_to=[
            customer_email,
        ],
    )

    try:

        email.send(
            fail_silently=False,
        )

    except Exception:

        messages.error(
            request,
            (
                "Your enquiry could not be sent. "
                "Please try again later."
            ),
        )

        return redirect(
            "rental_detail",
            slug=rental.slug,
        )

    messages.success(
        request,
        (
            "Your rental enquiry has been sent "
            "successfully to the owner."
        ),
    )

    return redirect(
        "rental_detail",
        slug=rental.slug,
    )


# ==========================================
# SECTION 4 END
# Submit Rental Enquiry
# ==========================================