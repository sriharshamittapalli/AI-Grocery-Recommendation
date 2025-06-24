BASE_PRICES = {
    'milk': 1.0, 'bread': 1.3, 'eggs': 1.6, 'bananas': 1.9, 'avocados': 2.2,
    'chicken breast': 2.5, 'rice': 2.8, 'pasta': 3.1, 'cheese': 3.4,
    'yogurt': 3.7, 'butter': 1.2, 'apples': 1.5, 'oranges': 1.8,
    'tomatoes': 2.1, 'lettuce': 2.4, 'cereal': 2.7, 'soda': 3.0,
    'coffee': 3.3, 'tea': 3.6, 'bacon': 3.9, 'sausage': 1.4,
    'ground beef': 1.7, 'pork chops': 2.0, 'oatmeal': 2.3, 'flour': 2.6,
    'sugar': 2.9, 'salt': 3.2, 'pepper': 3.5, 'olive oil': 3.8,
    'canola oil': 4.1, 'peanut butter': 1.6, 'jelly': 1.9,
    'canned beans': 2.2, 'canned corn': 2.5, 'canned tomatoes': 2.8,
    'pasta sauce': 3.1, 'ketchup': 3.4, 'mustard': 3.7, 'mayonnaise': 4.0,
    'grapes': 4.3, 'strawberries': 1.8, 'blueberries': 2.1,
    'spinach': 2.4, 'onions': 2.7, 'potatoes': 3.0, 'carrots': 3.3,
    'broccoli': 3.6, 'cucumbers': 3.9, 'peppers': 4.2, 'canned tuna': 4.5,
    'chips': 2.0, 'crackers': 2.3, 'cookies': 2.6, 'nuts': 2.9,
    'granola bars': 3.2, 'popcorn': 3.5, 'chocolate': 3.8,
    'ice cream': 4.1, 'bagels': 4.4, 'tortillas': 4.7
}

DEFAULT_MULTIPLIERS = {
    'Walmart': 0.9,
    'Target': 1.0,
    'Kroger': 0.95,
    'Costco': 0.85,
    'Whole Foods': 1.3,
    'Safeway': 1.05,
    'Meijer': 0.92,
}

def _generate_price_data(multipliers):
    return {
        item: {
            store: round(BASE_PRICES[item] * mult + ((idx % 5) * 0.05), 2)
            for store, mult in multipliers.items()
        }
        for idx, item in enumerate(BASE_PRICES)
    }

def get_scenario1_data():
    """Prices spread across stores to encourage multi-store shopping."""
    return _generate_price_data(DEFAULT_MULTIPLIERS)

def get_scenario2_data():
    """Prices heavily favor Walmart so single-store is best."""
    multi = dict(DEFAULT_MULTIPLIERS)
    multi.update({
        'Walmart': 0.75,
        'Target': 1.2,
        'Kroger': 1.15,
        'Costco': 1.1,
        'Whole Foods': 1.35,
        'Safeway': 1.25,
        'Meijer': 1.1,
    })
    return _generate_price_data(multi)

def get_scenario3_data():
    """Balanced prices useful for strict-mode tests."""
    return _generate_price_data(DEFAULT_MULTIPLIERS)
