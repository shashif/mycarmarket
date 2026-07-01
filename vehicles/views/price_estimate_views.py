# ==========================================
# MyCarMarket
# Version: v1.5.5
# File: vehicles/views/price_estimate_views.py
# Description: AI Smart Price Estimation API View
# ==========================================

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from vehicles.services.price_estimator import estimate_car_price


@login_required
def ai_price_estimate(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request method."
        }, status=405)

    estimate = estimate_car_price(
        make=request.POST.get("make"),
        model=request.POST.get("model"),
        year=request.POST.get("year"),
        kilometres=request.POST.get("kilometres"),
        transmission=request.POST.get("transmission"),
        fuel_type=request.POST.get("fuel_type"),
        body_type=request.POST.get("body_type"),
        condition=request.POST.get("condition"),
        state=request.POST.get("state"),
    )

    return JsonResponse(estimate)