# ==========================================
# MyCarMarket
# Version: v1.14.0
# File: amazon_affiliate/views.py
# Description: Amazon Accessories Store Views
# ==========================================

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import AmazonCategory, AmazonProduct


def amazon_product_list(request, category_slug=None):

    categories = AmazonCategory.objects.filter(
        is_active=True
    ).order_by(
        "display_order",
        "name"
    )

    products = AmazonProduct.objects.filter(
        is_active=True
    ).select_related(
        "product_category"
    )

    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(
            AmazonCategory,
            slug=category_slug,
            is_active=True
        )

        products = products.filter(
            product_category=selected_category
        )

    products = products.order_by(
        "-is_featured",
        "display_order",
        "title"
    )

    paginator = Paginator(products, 24)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        "selected_category": selected_category,
        "page_obj": page_obj,
    }

    return render(
        request,
        "amazon_affiliate/product_list.html",
        context
    )