# ==========================================
# MyCarMarket
# Version: v1.4.0
# File: vehicles/views/dealer_review_views.py
# Dealer Review Views
# ==========================================

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
)

from django.contrib.auth.models import User

from vehicles.models import (
    DealerReview,
)


@login_required
def add_review(request, username):

    dealer = get_object_or_404(
        User,
        username=username
    )

    if dealer == request.user:

        messages.error(
            request,
            'You cannot review yourself.'
        )

        return redirect(
            'dealer_detail',
            username=username
        )

    existing_review = DealerReview.objects.filter(
        dealer=dealer,
        reviewer=request.user
    ).first()

    if existing_review:

        messages.warning(
            request,
            'You have already reviewed this dealer.'
        )

        return redirect(
            'dealer_detail',
            username=username
        )

    if request.method == 'POST':

        rating = request.POST.get(
            'rating'
        )

        comment = request.POST.get(
            'comment'
        )

        if rating and comment:

            DealerReview.objects.create(
                dealer=dealer,
                reviewer=request.user,
                rating=rating,
                comment=comment
            )

            messages.success(
                request,
                'Review submitted successfully.'
            )

    return redirect(
        'dealer_detail',
        username=username
    )


@login_required
def edit_review(request, review_id):

    review = get_object_or_404(
        DealerReview,
        id=review_id,
        reviewer=request.user
    )

    if request.method == 'POST':

        review.rating = request.POST.get(
            'rating'
        )

        review.comment = request.POST.get(
            'comment'
        )

        review.save()

        messages.success(
            request,
            'Review updated successfully.'
        )

    return redirect(
        'dealer_detail',
        username=review.dealer.username
    )


@login_required
def delete_review(request, review_id):

    review = get_object_or_404(
        DealerReview,
        id=review_id,
        reviewer=request.user
    )

    dealer_username = review.dealer.username

    review.delete()

    messages.success(
        request,
        'Review deleted successfully.'
    )

    return redirect(
        'dealer_detail',
        username=dealer_username
    )