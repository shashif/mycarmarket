# ==========================================
# MyCarMarket
# Version: v1.5.5
# File: vehicles/services/price_estimator.py
# Description: AI Smart Price Estimation Service
# ==========================================

from decimal import Decimal
from django.db.models import Avg, Count
from vehicles.models import Car


def estimate_car_price(
    make=None,
    model=None,
    year=None,
    kilometres=None,
    transmission=None,
    fuel_type=None,
    body_type=None,
    condition=None,
    state=None
):
    try:
        year = int(year)
    except (TypeError, ValueError):
        year = None

    try:
        kilometres = int(kilometres)
    except (TypeError, ValueError):
        kilometres = None

    cars = Car.objects.filter(
        is_approved=True,
        is_active=True,
        moderation_status='approved',
        price__gt=0
    )

    if make:
        cars = cars.filter(make__iexact=make)

    if model:
        cars = cars.filter(model__iexact=model)

    if year:
        cars = cars.filter(year__gte=year - 2, year__lte=year + 2)

    if transmission:
        cars = cars.filter(transmission__iexact=transmission)

    if fuel_type:
        cars = cars.filter(fuel_type__iexact=fuel_type)

    if body_type:
        cars = cars.filter(body_type__iexact=body_type)

    if state:
        cars = cars.filter(state__iexact=state)

    result = cars.aggregate(
        average_price=Avg('price'),
        total_matches=Count('id')
    )

    average_price = result.get('average_price')
    total_matches = result.get('total_matches', 0)

    if not average_price:
        return {
            "success": False,
            "message": "Not enough similar vehicles found to estimate price."
        }

    estimated_price = Decimal(average_price)

    if kilometres:
        if kilometres < 50000:
            estimated_price *= Decimal("1.06")
        elif kilometres < 100000:
            estimated_price *= Decimal("1.02")
        elif kilometres > 180000:
            estimated_price *= Decimal("0.88")
        elif kilometres > 130000:
            estimated_price *= Decimal("0.94")

    if condition:
        condition_lower = condition.lower()

        if "excellent" in condition_lower:
            estimated_price *= Decimal("1.05")
        elif "good" in condition_lower:
            estimated_price *= Decimal("1.00")
        elif "fair" in condition_lower:
            estimated_price *= Decimal("0.93")
        elif "poor" in condition_lower:
            estimated_price *= Decimal("0.85")

    estimated_price = int(round(estimated_price / 100) * 100)

    low_price = int(round((estimated_price * Decimal("0.94")) / 100) * 100)
    high_price = int(round((estimated_price * Decimal("1.06")) / 100) * 100)

    if total_matches >= 20:
        confidence = 92
    elif total_matches >= 10:
        confidence = 82
    elif total_matches >= 5:
        confidence = 70
    else:
        confidence = 55

    return {
        "success": True,
        "estimated_price": estimated_price,
        "suggested_price": estimated_price,
        "low_price": low_price,
        "high_price": high_price,
        "confidence": confidence,
        "total_matches": total_matches,
    }