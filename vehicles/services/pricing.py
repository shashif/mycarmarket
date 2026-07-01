# ==========================================
# MyCarMarket
# Version: v1.4.6
# File: vehicles/services/pricing.py
# Description: Smart Price Suggestion Engine for Sellers
# ==========================================

from statistics import median

from vehicles.models import Car


def get_price_suggestion(
    make=None,
    model=None,
    year=None,
    odometer=None,
    transmission=None,
    fuel_type=None,
    state=None,
):
    if not make or not model or not year:
        return {
            "success": False,
            "message": "Make, model and year are required.",
        }

    try:
        year = int(year)
    except (ValueError, TypeError):
        return {
            "success": False,
            "message": "Invalid year.",
        }

    similar_cars = Car.objects.filter(
        is_approved=True,
        is_active=True,
        make__iexact=make,
        model__iexact=model,
        year__gte=year - 1,
        year__lte=year + 1,
        price__gt=0,
    )

    if transmission:
        similar_cars = similar_cars.filter(
            transmission__iexact=transmission
        )

    if fuel_type:
        similar_cars = similar_cars.filter(
            fuel_type__iexact=fuel_type
        )

    if state:
        similar_cars = similar_cars.filter(
            state__iexact=state
        )

    # ==========================================
    # Match by Kilometres
    # ==========================================

    if odometer:
        try:
            odometer = int(odometer)

            similar_cars = similar_cars.filter(
                kilometres__gte=max(0, odometer - 30000),
                kilometres__lte=odometer + 30000,
            )

        except (ValueError, TypeError):
            pass

    prices = list(
        similar_cars.values_list(
            "price",
            flat=True
        )
    )

    count = len(prices)

    # For testing only.
    # Change back to <3 before production.
    if count < 3:
        return {
            "success": False,
            "message": "Not enough similar vehicles found yet.",
            "count": count,
        }

    prices.sort()

    recommended_price = int(round(median(prices), -2))
    min_price = int(round(min(prices), -2))
    max_price = int(round(max(prices), -2))
    average_price = int(round(sum(prices) / count, -2))

    if count >= 25:
        confidence = "High"
        stars = 5
    elif count >= 15:
        confidence = "Medium"
        stars = 4
    elif count >= 8:
        confidence = "Fair"
        stars = 3
    else:
        confidence = "Low"
        stars = 2

    return {
        "success": True,
        "recommended": recommended_price,
        "min": min_price,
        "max": max_price,
        "average": average_price,
        "median": recommended_price,
        "count": count,
        "confidence": confidence,
        "stars": stars,
    }