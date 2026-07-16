
# MyCarMarket Australia
# Version: v2.2.5
# File: services/views.py
# Location: services/views.py
# Description:
# Car Services views with:
# - Public approved service listings
# - Search, category and location filters
# - Service detail pages
# - Secure service enquiry submission
# - Logged-in service listing creation
# - Provider email notifications
# - Pending listing confirmation emails
# - Listing view tracking
# - Global SiteSettings supplied to service templates
# - Custom and Google banner selection from admin
# Last Updated: 17 Jul 2026
# ==========================================


# ==========================================
# SECTION 1 START
# Imports
# ==========================================

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse

from core.models import SiteSettings

from services.forms import (
    CarServiceForm,
    ServiceEnquiryForm,
)
from services.models import (
    CarService,
    ServiceEnquiry,
)

# ==========================================
# SECTION 1 END
# Imports
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 2 START
# Helper Functions
# ==========================================

def get_client_ip(
    request,
):

    forwarded_for = request.META.get(
        "HTTP_X_FORWARDED_FOR",
        "",
    )

    if forwarded_for:

        return (
            forwarded_for
            .split(",")[0]
            .strip()
        )

    return request.META.get(
        "REMOTE_ADDR"
    )



def get_site_settings():

    return SiteSettings.objects.first()

def get_public_services_queryset():

    return (
        CarService.objects
        .filter(
            moderation_status="approved",
            is_approved=True,
            is_active=True,
        )
        .select_related(
            "posted_by",
        )
        .prefetch_related(
            "images",
        )
    )


def send_service_enquiry_email(
    enquiry,
):

    service = enquiry.service

    subject = (
        f"New service enquiry: "
        f"{service.title}"
    )

    service_url = ""

    try:

        service_url = (
            settings.SITE_URL.rstrip("/")
            + service.get_absolute_url()
        )

    except AttributeError:

        service_url = service.get_absolute_url()

    message = (
        f"Hello {service.provider_name},\n\n"
        f"You have received a new enquiry through "
        f"MyCarMarket Australia.\n\n"
        f"Service: {service.title}\n"
        f"Business: {service.business_name}\n"
        f"Customer: {enquiry.customer_name}\n"
        f"Email: {enquiry.customer_email}\n"
        f"Phone: {enquiry.customer_phone}\n\n"
        f"Message:\n"
        f"{enquiry.message}\n\n"
        f"Service listing:\n"
        f"{service_url}\n\n"
        f"Please contact the customer directly using "
        f"the details above.\n\n"
        f"Regards,\n"
        f"MyCarMarket Australia"
    )

    sender_email = getattr(
        settings,
        "DEFAULT_FROM_EMAIL",
        None,
    )

    if not sender_email:

        return False

    try:

        sent_count = send_mail(
            subject=subject,
            message=message,
            from_email=sender_email,
            recipient_list=[
                service.provider_email,
            ],
            fail_silently=False,
        )

        return sent_count > 0

    except Exception:

        return False


def send_service_listing_confirmation_email(
    service,
):

    subject = (
        "Your service listing is pending approval"
    )

    message = (
        f"Hello {service.provider_name},\n\n"
        f"Thank you for listing your service on "
        f"MyCarMarket Australia.\n\n"
        f"Listing: {service.title}\n"
        f"Business: {service.business_name}\n"
        f"Category: {service.get_category_display()}\n"
        f"Location: {service.location}\n\n"
        f"Your listing has been submitted and is now "
        f"pending administrator approval.\n\n"
        f"We will review the listing before it becomes "
        f"publicly available.\n\n"
        f"Regards,\n"
        f"MyCarMarket Australia"
    )

    sender_email = getattr(
        settings,
        "DEFAULT_FROM_EMAIL",
        None,
    )

    if not sender_email:

        return False

    try:

        sent_count = send_mail(
            subject=subject,
            message=message,
            from_email=sender_email,
            recipient_list=[
                service.provider_email,
            ],
            fail_silently=False,
        )

        return sent_count > 0

    except Exception:

        return False


# ==========================================
# SECTION 2 END
# Helper Functions
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 3 START
# Service List View
# ==========================================

def service_list(
    request,
):

    services = get_public_services_queryset()

    search_query = (
        request.GET
        .get(
            "search",
            "",
        )
        .strip()
    )

    category = (
        request.GET
        .get(
            "category",
            "",
        )
        .strip()
    )

    state = (
        request.GET
        .get(
            "state",
            "",
        )
        .strip()
    )

    suburb = (
        request.GET
        .get(
            "suburb",
            "",
        )
        .strip()
    )

    mobile_service = (
        request.GET
        .get(
            "mobile_service",
            "",
        )
        .strip()
    )

    sort = (
        request.GET
        .get(
            "sort",
            "featured",
        )
        .strip()
    )

    if search_query:

        services = services.filter(
            Q(
                title__icontains=search_query
            )
            | Q(
                business_name__icontains=search_query
            )
            | Q(
                description__icontains=search_query
            )
            | Q(
                suburb__icontains=search_query
            )
            | Q(
                postcode__icontains=search_query
            )
            | Q(
                service_area__icontains=search_query
            )
        )

    valid_categories = {
        choice[0]
        for choice
        in CarService.CATEGORY_CHOICES
    }

    if category in valid_categories:

        services = services.filter(
            category=category,
        )

    valid_states = {
        choice[0]
        for choice
        in CarService.STATE_CHOICES
    }

    if state in valid_states:

        services = services.filter(
            state=state,
        )

    if suburb:

        services = services.filter(
            suburb__icontains=suburb,
        )

    if mobile_service == "yes":

        services = services.filter(
            mobile_service=True,
        )

    elif mobile_service == "no":

        services = services.filter(
            mobile_service=False,
        )

    sort_options = {
        "featured": [
            "-is_featured",
            "-created_at",
        ],
        "newest": [
            "-created_at",
        ],
        "price_low": [
            "starting_price",
            "-is_featured",
        ],
        "price_high": [
            "-starting_price",
            "-is_featured",
        ],
        "popular": [
            "-views",
            "-created_at",
        ],
        "business": [
            "business_name",
            "title",
        ],
    }

    services = services.order_by(
        *sort_options.get(
            sort,
            sort_options["featured"],
        )
    )

    paginator = Paginator(
        services,
        12,
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    query_parameters = request.GET.copy()

    if "page" in query_parameters:

        query_parameters.pop(
            "page"
        )

    context = {
        "settings": get_site_settings(),
        "page_obj": page_obj,
        "services": page_obj.object_list,
        "search_query": search_query,
        "selected_category": category,
        "selected_state": state,
        "selected_suburb": suburb,
        "selected_mobile_service": (
            mobile_service
        ),
        "selected_sort": sort,
        "category_choices": (
            CarService.CATEGORY_CHOICES
        ),
        "state_choices": (
            CarService.STATE_CHOICES
        ),
        "query_string": (
            query_parameters.urlencode()
        ),
        "total_services": (
            paginator.count
        ),
    }

    return render(
        request,
        "services/service_list.html",
        context,
    )


# ==========================================
# SECTION 3 END
# Service List View
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 4 START
# Service Detail View
# ==========================================

def service_detail(
    request,
    slug,
):

    service = get_object_or_404(
        get_public_services_queryset(),
        slug=slug,
    )

    session_key = (
        f"service_viewed_{service.pk}"
    )

    if not request.session.get(
        session_key
    ):

        CarService.objects.filter(
            pk=service.pk,
        ).update(
            views=F("views") + 1,
        )

        request.session[
            session_key
        ] = True

        request.session.modified = True

        service.refresh_from_db(
            fields=[
                "views",
            ],
        )

    enquiry_form = (
        ServiceEnquiryForm()
    )

    related_services = (
        get_public_services_queryset()
        .filter(
            category=service.category,
        )
        .exclude(
            pk=service.pk,
        )
        .order_by(
            "-is_featured",
            "-created_at",
        )[:4]
    )

    context = {
        "settings": get_site_settings(),
        "service": service,
        "enquiry_form": enquiry_form,
        "related_services": (
            related_services
        ),
    }

    return render(
        request,
        "services/service_detail.html",
        context,
    )


# ==========================================
# SECTION 4 END
# Service Detail View
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 5 START
# Service Enquiry View
# ==========================================

def submit_service_enquiry(
    request,
    slug,
):

    if request.method != "POST":

        return redirect(
            "service_detail",
            slug=slug,
        )

    service = get_object_or_404(
        get_public_services_queryset(),
        slug=slug,
    )

    enquiry_form = ServiceEnquiryForm(
        request.POST,
    )

    if enquiry_form.is_valid():

        with transaction.atomic():

            enquiry = enquiry_form.save(
                commit=False,
            )

            enquiry.service = service

            enquiry.customer_ip_address = (
                get_client_ip(
                    request
                )
            )

            enquiry.user_agent = (
                request.META.get(
                    "HTTP_USER_AGENT",
                    "",
                )[:1000]
            )

            enquiry.save()

        provider_notified = (
            send_service_enquiry_email(
                enquiry
            )
        )

        if provider_notified:

            ServiceEnquiry.objects.filter(
                pk=enquiry.pk,
            ).update(
                provider_notified=True,
            )

        messages.success(
            request,
            (
                "Your enquiry has been sent "
                "successfully. The service provider "
                "will contact you directly."
            ),
        )

        return redirect(
            f"{reverse('service_detail', kwargs={'slug': service.slug})}"
            "#service-enquiry"
        )

    related_services = (
        get_public_services_queryset()
        .filter(
            category=service.category,
        )
        .exclude(
            pk=service.pk,
        )
        .order_by(
            "-is_featured",
            "-created_at",
        )[:4]
    )

    messages.error(
        request,
        (
            "Please correct the errors in the "
            "enquiry form."
        ),
    )

    context = {
        "settings": get_site_settings(),
        "service": service,
        "enquiry_form": enquiry_form,
        "related_services": (
            related_services
        ),
    }

    return render(
        request,
        "services/service_detail.html",
        context,
        status=400,
    )


# ==========================================
# SECTION 5 END
# Service Enquiry View
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 6 START
# Create Service Listing View
# ==========================================

@login_required
def create_service(
    request,
):

    if request.method == "POST":

        form = CarServiceForm(
            request.POST,
            request.FILES,
            request=request,
        )

        if form.is_valid():

            with transaction.atomic():

                service = form.save(
                    commit=True,
                )

            send_service_listing_confirmation_email(
                service
            )

            messages.success(
                request,
                (
                    "Your service listing has been "
                    "submitted successfully and is "
                    "pending administrator approval."
                ),
            )

            return redirect(
                "service_submission_success"
            )

        messages.error(
            request,
            (
                "Please correct the errors below "
                "and submit the form again."
            ),
        )

    else:

        initial_data = {}

        full_name = (
            request.user
            .get_full_name()
            .strip()
        )

        if full_name:

            initial_data[
                "provider_name"
            ] = full_name

        if request.user.email:

            initial_data[
                "provider_email"
            ] = request.user.email

        form = CarServiceForm(
            initial=initial_data,
            request=request,
        )

    context = {
        "settings": get_site_settings(),
        "form": form,
        "category_choices": (
            CarService.CATEGORY_CHOICES
        ),
        "state_choices": (
            CarService.STATE_CHOICES
        ),
    }

    return render(
        request,
        "services/create_service.html",
        context,
    )


# ==========================================
# SECTION 6 END
# Create Service Listing View
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 7 START
# Service Submission Success View
# ==========================================

@login_required
def service_submission_success(
    request,
):

    return render(
        request,
        (
            "services/"
            "service_submission_success.html"
        ),
    )


# ==========================================
# SECTION 7 END
# Service Submission Success View
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 8 START
# User Service Listings View
# ==========================================

@login_required
def my_service_listings(
    request,
):

    services = (
        CarService.objects
        .filter(
            posted_by=request.user,
        )
        .prefetch_related(
            "images",
        )
        .order_by(
            "-created_at",
        )
    )

    paginator = Paginator(
        services,
        10,
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    context = {
        "settings": get_site_settings(),
        "page_obj": page_obj,
        "services": page_obj.object_list,
        "total_services": paginator.count,
    }

    return render(
        request,
        "services/my_service_listings.html",
        context,
    )


# ==========================================
# SECTION 8 END
# User Service Listings View
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 9 START
# Edit Service Listing View
# ==========================================

@login_required
def edit_service(
    request,
    slug,
):

    service = get_object_or_404(
        CarService.objects.prefetch_related(
            "images",
        ),
        slug=slug,
        posted_by=request.user,
    )

    if request.method == "POST":

        form = CarServiceForm(
            request.POST,
            request.FILES,
            instance=service,
            request=request,
        )

        if form.is_valid():

            with transaction.atomic():

                service = form.save(
                    commit=True,
                )

            messages.success(
                request,
                (
                    "Your service listing has been "
                    "updated and returned to pending "
                    "approval."
                ),
            )

            return redirect(
                "my_service_listings"
            )

        messages.error(
            request,
            (
                "Please correct the errors below "
                "and submit the form again."
            ),
        )

    else:

        form = CarServiceForm(
            instance=service,
            request=request,
        )

    context = {
        "settings": get_site_settings(),
        "form": form,
        "service": service,
        "is_editing": True,
        "category_choices": (
            CarService.CATEGORY_CHOICES
        ),
        "state_choices": (
            CarService.STATE_CHOICES
        ),
    }

    return render(
        request,
        "services/create_service.html",
        context,
    )


# ==========================================
# SECTION 9 END
# Edit Service Listing View
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 10 START
# Service Owner Preview View
# ==========================================

@login_required
def service_owner_preview(
    request,
    slug,
):

    service = get_object_or_404(
        CarService.objects
        .select_related(
            "posted_by",
        )
        .prefetch_related(
            "images",
        ),
        slug=slug,
        posted_by=request.user,
    )

    enquiry_form = (
        ServiceEnquiryForm()
    )

    context = {
        "settings": get_site_settings(),
        "service": service,
        "enquiry_form": enquiry_form,
        "related_services": [],
        "owner_preview": True,
    }

    return render(
        request,
        "services/service_detail.html",
        context,
    )


# ==========================================
# SECTION 10 END
# Service Owner Preview View
# ==========================================

# ---------------------------------------------


# ==========================================
# SECTION 11 START
# Delete Service Listing View
# ==========================================

@login_required
def delete_service(
    request,
    slug,
):

    service = get_object_or_404(
        CarService,
        slug=slug,
        posted_by=request.user,
    )

    if request.method == "POST":

        service_title = (
            service.title
        )

        service.delete()

        messages.success(
            request,
            (
                f'"{service_title}" has been '
                f"deleted successfully."
            ),
        )

        return redirect(
            "my_service_listings"
        )

    context = {
        "settings": get_site_settings(),
        "service": service,
    }

    return render(
        request,
        "services/delete_service.html",
        context,
    )


# ==========================================
# SECTION 11 END
# Delete Service Listing View
# ==========================================