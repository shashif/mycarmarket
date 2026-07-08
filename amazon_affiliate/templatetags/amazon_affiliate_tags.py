# ==========================================
# MyCarMarket
# Version: v1.13.0
# File: amazon_affiliate/templatetags/amazon_affiliate_tags.py
# Description: Amazon Affiliate Template Tags
# ==========================================

from django import template
from amazon_affiliate.models import AmazonProduct

register = template.Library()


@register.simple_tag
def get_amazon_products(body_type=None, limit=4):

    products = AmazonProduct.objects.filter(
        is_active=True
    )

    if body_type:
        body_type = str(body_type).lower().strip()

        products = products.filter(
            body_type__in=[
                body_type,
                "all",
            ]
        )
    else:
        products = products.filter(
            body_type="all"
        )

    return products.order_by(
        "-is_featured",
        "display_order",
        "title"
    )[:limit]