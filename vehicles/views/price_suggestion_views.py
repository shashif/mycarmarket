# ==========================================
# MyCarMarket
# Version: v1.4.6
# File: vehicles/views/price_suggestion_views.py
# Description: Smart Price Suggestion API View
# ==========================================

from django.http import JsonResponse

from vehicles.services.pricing import get_price_suggestion


def price_suggestion_api(request):
    suggestion = get_price_suggestion(
        make=request.GET.get("make"),
        model=request.GET.get("model"),
        year=request.GET.get("year"),
        odometer=request.GET.get("odometer"),
        transmission=request.GET.get("transmission"),
        fuel_type=request.GET.get("fuel_type"),
        state=request.GET.get("state"),
    )

    return JsonResponse(suggestion)