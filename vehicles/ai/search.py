# ==========================================
# MyCarMarket
# Version: v1.5.4
# File: vehicles/ai/search.py
# Description: AI Smart Search Engine for Vehicle Search
# ==========================================

import re

from django.db.models import Q


def parse_ai_vehicle_search(query):

    original_query = query or ''
    query_lower = original_query.lower().strip()

    filters = {
        'max_price': '',
        'min_price': '',
        'body_type': '',
        'transmission': '',
        'fuel_type': '',
        'state': '',
        'keywords': '',
        'notes': [],
    }

    price_match = re.search(
        r'(under|below|less than|max|up to)\s*\$?\s*(\d+)\s*k?',
        query_lower
    )

    if price_match:
        price_value = int(price_match.group(2))

        if price_value < 1000:
            price_value *= 1000

        filters['max_price'] = str(price_value)
        filters['notes'].append(f'Budget: under ${price_value:,}')
        query_lower = query_lower.replace(price_match.group(0), ' ')

    body_map = {
        'family suv': 'SUV',
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

    for word, value in body_map.items():
        if word in query_lower:
            filters['body_type'] = value
            filters['notes'].append(f'Body type: {value}')
            query_lower = query_lower.replace(word, ' ')
            break

    if 'automatic' in query_lower or 'auto' in query_lower:
        filters['transmission'] = 'Automatic'
        filters['notes'].append('Transmission: Automatic')
        query_lower = query_lower.replace('automatic', ' ')
        query_lower = query_lower.replace('auto', ' ')

    if 'manual' in query_lower:
        filters['transmission'] = 'Manual'
        filters['notes'].append('Transmission: Manual')
        query_lower = query_lower.replace('manual', ' ')

    fuel_map = {
        'petrol': 'Petrol',
        'diesel': 'Diesel',
        'hybrid': 'Hybrid',
        'electric': 'Electric',
        'ev': 'Electric',
        'lpg': 'LPG',
    }

    for word, value in fuel_map.items():
        if word in query_lower:
            filters['fuel_type'] = value
            filters['notes'].append(f'Fuel: {value}')
            query_lower = query_lower.replace(word, ' ')
            break

    state_map = {
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

    for word, value in state_map.items():
        if word in query_lower:
            filters['state'] = value
            filters['notes'].append(f'State: {value}')
            query_lower = query_lower.replace(word, ' ')
            break

    intent_words = [
        'actually',
        'i',
        'want',
        'need',
        'looking',
        'for',
        'find',
        'show',
        'me',
        'family',
        'first',
        'car',
        'cars',
        'vehicle',
        'vehicles',
        'best',
        'good',
        'reliable',
        'safe',
        'cheap',
        'budget',
        'affordable',
        'daily',
        'work',
        'student',
        'in',
        'near',
        'around',
        'with',
        'and',
        'the',
        'a',
        'an',
    ]

    words = query_lower.split()

    cleaned_words = [
        word for word in words
        if word not in intent_words
    ]

    filters['keywords'] = ' '.join(cleaned_words).strip()

    return filters


def apply_ai_vehicle_search(cars, query, current_filters=None):

    current_filters = current_filters or {}

    ai_filters = parse_ai_vehicle_search(query)

    max_price = current_filters.get('max_price') or ai_filters['max_price']
    min_price = current_filters.get('min_price') or ai_filters['min_price']
    body_type = current_filters.get('body_type') or ai_filters['body_type']
    transmission = current_filters.get('transmission') or ai_filters['transmission']
    fuel_type = current_filters.get('fuel_type') or ai_filters['fuel_type']
    state = current_filters.get('state') or ai_filters['state']

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)

    if body_type:
        cars = cars.filter(body_type=body_type)

    if transmission:
        cars = cars.filter(transmission=transmission)

    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)

    if state:
        cars = cars.filter(state=state)

    keywords = ai_filters['keywords']

    if keywords:
        cars = cars.filter(
            Q(title__icontains=keywords) |
            Q(make__icontains=keywords) |
            Q(model__icontains=keywords) |
            Q(suburb__icontains=keywords) |
            Q(state__icontains=keywords) |
            Q(description__icontains=keywords)
        )

    final_filters = {
        'max_price': max_price,
        'min_price': min_price,
        'body_type': body_type,
        'transmission': transmission,
        'fuel_type': fuel_type,
        'state': state,
        'keywords': keywords,
        'notes': ai_filters['notes'],
    }

    return cars, final_filters