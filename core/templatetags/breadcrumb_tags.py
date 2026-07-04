# ==========================================
# MyCarMarket
# Version: v1.7.8
# File: core/templatetags/breadcrumb_tags.py
# Description: Global Breadcrumb Navigation + BreadcrumbList Schema
# ==========================================

import json

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def breadcrumb(context, *items):
    request = context.get("request")

    breadcrumb_items = []

    for index in range(0, len(items), 2):
        name = str(items[index]).strip()

        url = ""
        if index + 1 < len(items):
            url = str(items[index + 1]).strip()

        if not name:
            continue

        breadcrumb_items.append({
            "name": name,
            "url": url,
        })

    if not breadcrumb_items:
        return ""

    nav_html = '<nav class="mcm-breadcrumb" aria-label="Breadcrumb">'
    nav_html += '<ol class="mcm-breadcrumb-list">'

    schema_items = []

    for position, item in enumerate(breadcrumb_items, start=1):
        name = escape(item["name"])
        url = item["url"]
        is_last = position == len(breadcrumb_items)

        if url and not is_last:
            nav_html += (
                '<li class="mcm-breadcrumb-item">'
                f'<a href="{escape(url)}">{name}</a>'
                '</li>'
            )
        else:
            nav_html += (
                '<li class="mcm-breadcrumb-item active" aria-current="page">'
                f'{name}'
                '</li>'
            )

        schema_item = {
            "@type": "ListItem",
            "position": position,
            "name": item["name"],
        }

        if url:
            if request:
                schema_item["item"] = request.build_absolute_uri(url)
            else:
                schema_item["item"] = url

        schema_items.append(schema_item)

    nav_html += "</ol></nav>"

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": schema_items,
    }

    schema_html = (
        '<script type="application/ld+json">'
        f'{json.dumps(schema, ensure_ascii=False)}'
        '</script>'
    )

    return mark_safe(nav_html + schema_html)