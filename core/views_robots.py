# ==========================================
# MyCarMarket
# Version: v0.8.2
# File: core/views_robots.py
# Robots.txt SEO File
# ==========================================

from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "Sitemap: https://mycarmarket.com.au/sitemap.xml",
    ]

    return HttpResponse(
        "\n".join(lines),
        content_type="text/plain"
    )