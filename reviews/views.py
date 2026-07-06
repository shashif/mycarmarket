# ==========================================
# MyCarMarket
# Version: v1.10.5
# File: reviews/views.py
# Description: Review List and Detail Views + SiteSettings Ads Context
# ==========================================

from django.shortcuts import get_object_or_404, render

from core.models import SiteSettings

from .models import CarReview


# ==========================================
# SECTION 01: REVIEW LIST VIEW
# START
# ==========================================

def review_list(request):

    site_settings = SiteSettings.objects.first()

    reviews = CarReview.objects.filter(
        is_published=True
    ).order_by('-published_at')

    featured_reviews = reviews.filter(
        is_featured=True
    )[:3]

    context = {
        'reviews': reviews,
        'featured_reviews': featured_reviews,
        'settings': site_settings,
    }

    return render(
        request,
        'reviews/review_list.html',
        context
    )

# ==========================================
# SECTION 01: REVIEW LIST VIEW
# END
# ==========================================


# ==========================================
# SECTION 02: REVIEW DETAIL VIEW
# START
# ==========================================

def review_detail(request, slug):

    site_settings = SiteSettings.objects.first()

    review = get_object_or_404(
        CarReview,
        slug=slug,
        is_published=True
    )

    related_reviews = CarReview.objects.filter(
        is_published=True,
        make__iexact=review.make
    ).exclude(
        id=review.id
    )[:4]

    context = {
        'review': review,
        'related_reviews': related_reviews,
        'settings': site_settings,
    }

    return render(
        request,
        'reviews/review_detail.html',
        context
    )

# ==========================================
# SECTION 02: REVIEW DETAIL VIEW
# END
# ==========================================