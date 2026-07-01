# ==========================================
# MyCarMarket
# Version: v1.5.6
# File: vehicles/services/pricing.py
# Description: Professional AI Smart Price Estimation Fallback Engine
# ==========================================

from statistics import median

from vehicles.models import Car


def _clean_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _round_price(value):
    return int(round(value, -2))


def _get_confidence(count, fallback_level):
    if count >= 25 and fallback_level <= 2:
        return "High", 5

    if count >= 10 and fallback_level <= 3:
        return "Medium", 4

    if count >= 5:
        return "Fair", 3

    if count >= 1:
        return "Low", 2

    return "Very Low", 1


def _build_result(prices, count, fallback_label, fallback_level):
    prices.sort()

    recommended_price = _round_price(median(prices))
    min_price = _round_price(recommended_price * 0.94)
    max_price = _round_price(recommended_price * 1.06)
    average_price = _round_price(sum(prices) / count)

    confidence, stars = _get_confidence(count, fallback_level)

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
        "fallback_label": fallback_label,
    }


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

    year = _clean_int(year)
    odometer = _clean_int(odometer)

    if not year:
        return {
            "success": False,
            "message": "Invalid year.",
        }

    base_cars = Car.objects.filter(
        is_approved=True,
        is_active=True,
        price__gt=0,
    )

    search_levels = []

    level_1 = base_cars.filter(
        make__iexact=make,
        model__iexact=model,
        year__gte=year - 1,
        year__lte=year + 1,
    )

    if transmission:
        level_1 = level_1.filter(transmission__iexact=transmission)

    if fuel_type:
        level_1 = level_1.filter(fuel_type__iexact=fuel_type)

    if state:
        level_1 = level_1.filter(state__iexact=state)

    if odometer:
        level_1 = level_1.filter(
            kilometres__gte=max(0, odometer - 30000),
            kilometres__lte=odometer + 30000,
        )

    search_levels.append((
        level_1,
        "Very similar vehicles",
        1,
    ))

    search_levels.append((
        base_cars.filter(
            make__iexact=make,
            model__iexact=model,
            year__gte=year - 2,
            year__lte=year + 2,
        ),
        "Same make and model within nearby years",
        2,
    ))

    search_levels.append((
        base_cars.filter(
            make__iexact=make,
            model__iexact=model,
        ),
        "Same make and model",
        3,
    ))

    search_levels.append((
        base_cars.filter(
            make__iexact=make,
            year__gte=year - 3,
            year__lte=year + 3,
        ),
        "Same make with nearby years",
        4,
    ))

    search_levels.append((
        base_cars.filter(
            year__gte=year - 3,
            year__lte=year + 3,
        ),
        "Broader market with nearby years",
        5,
    ))

    search_levels.append((
        base_cars,
        "Overall MyCarMarket approved listings",
        6,
    ))

    for queryset, label, fallback_level in search_levels:
        prices = list(queryset.values_list("price", flat=True))
        count = len(prices)

        if count >= 1:
            return _build_result(
                prices=prices,
                count=count,
                fallback_label=label,
                fallback_level=fallback_level,
            )

    return {
        "success": False,
        "message": "No approved vehicle price data available yet.",
        "count": 0,
    }