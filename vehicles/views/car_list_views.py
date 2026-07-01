# ==========================================
# MyCarMarket
# Version: v1.5.4
# File: vehicles/views/car_list_views.py
# Description: Public Car List + Moderation Filter + AI Smart Search Fixed State Detection
# ==========================================

import re

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from vehicles.models import Car, FavouriteCar


# ==========================================
# SECTION 01: AI SEARCH HELPER
# START
# ==========================================

def parse_ai_search(query):

    query_lower = query.lower().strip()

    ai_filters = {
        'max_price': '',
        'min_price': '',
        'body_type': '',
        'transmission': '',
        'fuel_type': '',
        'state': '',
        'keywords': '',
        'ai_notes': [],
    }

    # ==========================================
    # PRICE DETECTION
    # ==========================================

    price_match = re.search(
        r'\b(under|below|less than|max|up to)\b\s*\$?\s*(\d+)\s*k?',
        query_lower
    )

    if price_match:
        number = int(price_match.group(2))

        if number < 1000:
            number = number * 1000

        ai_filters['max_price'] = str(number)
        ai_filters['ai_notes'].append(
            f"Budget detected: under ${number:,}"
        )

        query_lower = query_lower.replace(
            price_match.group(0),
            ' '
        )

    budget_words = {
        'cheap': 15000,
        'budget': 20000,
        'affordable': 25000,
        'low price': 20000,
    }

    for word, value in budget_words.items():
        pattern = r'\b' + re.escape(word) + r'\b'

        if re.search(pattern, query_lower) and not ai_filters['max_price']:
            ai_filters['max_price'] = str(value)
            ai_filters['ai_notes'].append(
                f"Budget intent detected: under ${value:,}"
            )
            query_lower = re.sub(pattern, ' ', query_lower)

    # ==========================================
    # BODY TYPE DETECTION
    # ==========================================

    body_types = {
        'family suv': 'SUV',
        'family car': 'SUV',
        'suv': 'SUV',
        'sedan': 'Sedan',
        'hatchback': 'Hatchback',
        'hatch': 'Hatchback',
        'ute': 'Ute',
        'pickup': 'Ute',
        'coupe': 'Coupe',
        'convertible': 'Convertible',
        'wagon': 'Wagon',
        'van': 'Van',
    }

    for word, value in body_types.items():
        pattern = r'\b' + re.escape(word) + r'\b'

        if re.search(pattern, query_lower):
            ai_filters['body_type'] = value
            ai_filters['ai_notes'].append(
                f"Body type detected: {value}"
            )
            query_lower = re.sub(pattern, ' ', query_lower)
            break

    # ==========================================
    # TRANSMISSION DETECTION
    # ==========================================

    if re.search(r'\b(automatic|auto)\b', query_lower):
        ai_filters['transmission'] = 'Automatic'
        ai_filters['ai_notes'].append(
            'Transmission detected: Automatic'
        )
        query_lower = re.sub(r'\b(automatic|auto)\b', ' ', query_lower)

    if re.search(r'\bmanual\b', query_lower):
        ai_filters['transmission'] = 'Manual'
        ai_filters['ai_notes'].append(
            'Transmission detected: Manual'
        )
        query_lower = re.sub(r'\bmanual\b', ' ', query_lower)

    # ==========================================
    # FUEL TYPE DETECTION
    # ==========================================

    fuel_types = {
        'petrol': 'Petrol',
        'diesel': 'Diesel',
        'hybrid': 'Hybrid',
        'electric': 'Electric',
        'ev': 'Electric',
        'lpg': 'LPG',
    }

    for word, value in fuel_types.items():
        pattern = r'\b' + re.escape(word) + r'\b'

        if re.search(pattern, query_lower):
            ai_filters['fuel_type'] = value
            ai_filters['ai_notes'].append(
                f"Fuel type detected: {value}"
            )
            query_lower = re.sub(pattern, ' ', query_lower)
            break

    # ==========================================
    # STATE DETECTION
    # IMPORTANT:
    # Uses word boundary matching so "want" does not trigger WA or NT.
    # ==========================================

    states = {
        'victoria': 'VIC',
        'vic': 'VIC',
        'new south wales': 'NSW',
        'nsw': 'NSW',
        'queensland': 'QLD',
        'qld': 'QLD',
        'south australia': 'SA',
        'sa': 'SA',
        'western australia': 'WA',
        'wa': 'WA',
        'tasmania': 'TAS',
        'tas': 'TAS',
        'act': 'ACT',
        'northern territory': 'NT',
        'nt': 'NT',
    }

    for word, value in states.items():
        pattern = r'\b' + re.escape(word) + r'\b'

        if re.search(pattern, query_lower):
            ai_filters['state'] = value
            ai_filters['ai_notes'].append(
                f"State detected: {value}"
            )
            query_lower = re.sub(pattern, ' ', query_lower)
            break

    # ==========================================
    # INTENT WORD CLEANUP
    # ==========================================

    intent_words = [
        'actually',
        'i',
        'want',
        'need',
        'looking',
        'show',
        'me',
        'family',
        'first car',
        'first',
        'best',
        'good',
        'reliable',
        'safe',
        'safety',
        'daily',
        'commuter',
        'work',
        'school',
        'student',
        'luxury',
        'sport',
        'sports',
        'car',
        'cars',
        'vehicle',
        'vehicles',
        'in',
        'near',
        'around',
        'for',
        'with',
        'and',
        'the',
        'a',
        'an',
    ]

    for word in intent_words:
        pattern = r'\b' + re.escape(word) + r'\b'
        query_lower = re.sub(pattern, ' ', query_lower)

    query_lower = re.sub(r'\s+', ' ', query_lower).strip()

    ai_filters['keywords'] = query_lower

    return ai_filters

# ==========================================
# SECTION 01: AI SEARCH HELPER
# END
# ==========================================


# ==========================================
# SECTION 02: CAR LIST VIEW
# START
# ==========================================

def car_list(request):

    cars = Car.objects.filter(
        is_approved=True,
        is_active=True,
        moderation_status='approved'
    )

    query = request.GET.get('q', '').strip()

    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    min_year = request.GET.get('min_year', '').strip()
    max_year = request.GET.get('max_year', '').strip()

    suburb = request.GET.get('suburb', '').strip()
    state = request.GET.get('state', '').strip()

    transmission = request.GET.get('transmission', '').strip()
    fuel_type = request.GET.get('fuel_type', '').strip()
    body_type = request.GET.get('body_type', '').strip()

    featured = request.GET.get('featured', '').strip()
    sort_by = request.GET.get('sort_by', 'newest').strip()

    ai_search_notes = []

    # ==========================================
    # SECTION 03: AI SMART SEARCH
    # START
    # ==========================================

    if query:
        ai_filters = parse_ai_search(query)

        ai_search_notes = ai_filters['ai_notes']

        if not max_price and ai_filters['max_price']:
            max_price = ai_filters['max_price']

        if not min_price and ai_filters['min_price']:
            min_price = ai_filters['min_price']

        if not body_type and ai_filters['body_type']:
            body_type = ai_filters['body_type']

        if not transmission and ai_filters['transmission']:
            transmission = ai_filters['transmission']

        if not fuel_type and ai_filters['fuel_type']:
            fuel_type = ai_filters['fuel_type']

        if not state and ai_filters['state']:
            state = ai_filters['state']

        cleaned_query = ai_filters['keywords']

        if cleaned_query:
            cars = cars.filter(
                Q(title__icontains=cleaned_query) |
                Q(make__icontains=cleaned_query) |
                Q(model__icontains=cleaned_query) |
                Q(suburb__icontains=cleaned_query) |
                Q(state__icontains=cleaned_query) |
                Q(description__icontains=cleaned_query)
            )

    # ==========================================
    # SECTION 03: AI SMART SEARCH
    # END
    # ==========================================

    # ==========================================
    # SECTION 04: NORMAL FILTERS
    # START
    # ==========================================

    if featured == '1':
        cars = cars.filter(is_featured=True)

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)

    if min_year:
        cars = cars.filter(year__gte=min_year)

    if max_year:
        cars = cars.filter(year__lte=max_year)

    if suburb:
        cars = cars.filter(suburb__icontains=suburb)

    if state:
        cars = cars.filter(state=state)

    if transmission:
        cars = cars.filter(transmission=transmission)

    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)

    if body_type:
        cars = cars.filter(body_type=body_type)

    # ==========================================
    # SECTION 04: NORMAL FILTERS
    # END
    # ==========================================

    # ==========================================
    # SECTION 05: SORTING
    # START
    # ==========================================

    if sort_by == 'oldest':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            'created_at'
        )

    elif sort_by == 'price_low':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            'price'
        )

    elif sort_by == 'price_high':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            '-price'
        )

    elif sort_by == 'km_low':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            'kilometres'
        )

    elif sort_by == 'km_high':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            '-kilometres'
        )

    elif sort_by == 'year_new':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            '-year'
        )

    elif sort_by == 'year_old':
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            'year'
        )

    else:
        cars = cars.order_by(
            '-is_featured',
            '-is_verified_listing',
            '-created_at'
        )

    # ==========================================
    # SECTION 05: SORTING
    # END
    # ==========================================

    # ==========================================
    # SECTION 06: FAVOURITES
    # START
    # ==========================================

    favourite_car_ids = []

    if request.user.is_authenticated:

        favourite_car_ids = list(
            FavouriteCar.objects.filter(
                user=request.user
            ).values_list(
                'car_id',
                flat=True
            )
        )

    # ==========================================
    # SECTION 06: FAVOURITES
    # END
    # ==========================================

    # ==========================================
    # SECTION 07: PAGINATION + RENDER
    # START
    # ==========================================

    paginator = Paginator(cars, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'vehicles/car_list.html',
        {
            'cars': page_obj,
            'page_obj': page_obj,
            'query': query,
            'min_price': min_price,
            'max_price': max_price,
            'min_year': min_year,
            'max_year': max_year,
            'suburb': suburb,
            'state': state,
            'transmission': transmission,
            'fuel_type': fuel_type,
            'body_type': body_type,
            'featured': featured,
            'sort_by': sort_by,
            'favourite_car_ids': favourite_car_ids,
            'ai_search_notes': ai_search_notes,
        }
    )

# ==========================================
# SECTION 07: PAGINATION + RENDER
# END
# ==========================================


# ==========================================
# SECTION 02: CAR LIST VIEW
# END
# ==========================================


# ==========================================
# END FILE
# ==========================================