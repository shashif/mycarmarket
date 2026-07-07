# ==========================================
# MyCarMarket
# Version: v1.11.6
# File: reviews/views.py
# Description:
# Car reviews list and detail views with pagination,
# search, make filter and homepage ad settings support.
# ==========================================

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from core.models import SiteSettings
from reviews.models import CarReview


def review_list(request):

    q = request.GET.get("q", "").strip()
    selected_make = request.GET.get("make", "").strip()

    review_queryset = CarReview.objects.filter(
        is_published=True
    )

    if q:
        review_queryset = review_queryset.filter(
            Q(title__icontains=q) |
            Q(make__icontains=q) |
            Q(model__icontains=q) |
            Q(summary__icontains=q) |
            Q(content__icontains=q)
        )

    if selected_make:
        review_queryset = review_queryset.filter(
            make__iexact=selected_make
        )

    review_queryset = review_queryset.order_by(
        "-is_featured",
        "-published_at"
    )

    make_list = CarReview.objects.filter(
        is_published=True
    ).order_by(
        "make"
    ).values_list(
        "make",
        flat=True
    ).distinct()

    paginator = Paginator(review_queryset, 12)

    page_number = request.GET.get("page")
    reviews = paginator.get_page(page_number)

    settings = SiteSettings.objects.first()

    return render(
        request,
        "reviews/review_list.html",
        {
            "reviews": reviews,
            "settings": settings,
            "q": q,
            "selected_make": selected_make,
            "make_list": make_list,
        }
    )


def review_detail(request, slug):

    review = get_object_or_404(
        CarReview,
        slug=slug,
        is_published=True
    )

    related_reviews = CarReview.objects.filter(
        is_published=True,
        make=review.make
    ).exclude(
        id=review.id
    ).order_by(
        "-published_at"
    )[:3]

    settings = SiteSettings.objects.first()

    return render(
        request,
        "reviews/review_detail.html",
        {
            "review": review,
            "related_reviews": related_reviews,
            "settings": settings,
        }
    )