EMISSION_FACTORS = {
    'electricity': 0.5,    # kg CO2 per kWh (adjust using real-time API)
    'car': 0.404,          # kg CO2 per mile (gasoline)
    'diet': {
        1: 3.3,  # Meat-heavy diet (kg CO2/day)
        2: 2.5,
        3: 1.9,
        4: 1.4,
        5: 1.0   # Vegan diet
    },
    'flights': 90          # kg CO2 per hour of flying
}

def calculate_footprint(activity_data):
    """Calculate total carbon footprint."""
    electricity = activity_data['electricity_kwh'] * EMISSION_FACTORS['electricity']
    car = activity_data['miles_driven'] * EMISSION_FACTORS['car']
    diet = EMISSION_FACTORS['diet'][activity_data['diet_score']] * 30  # Monthly
    flights = activity_data['flights_hours'] * EMISSION_FACTORS['flights']
    return electricity + car + diet + flights
