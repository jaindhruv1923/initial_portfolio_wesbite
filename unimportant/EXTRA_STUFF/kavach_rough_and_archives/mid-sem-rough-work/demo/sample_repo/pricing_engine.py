"""
Algorithmic Ride-Hailing Pricing & Surge Multiplier Service.
"""

def calculate_base_fare(distance_km: float, time_minutes: float) -> float:
    """Calculates flat standard fare from trip duration and distance."""
    base_flag_fall = 35.0
    km_rate = 14.5
    minute_rate = 2.0
    return round(base_flag_fall + (distance_km * km_rate) + (time_minutes * minute_rate), 2)

def compute_dynamic_surge(demand: int, supply: int, base_fare: float) -> float:
    """Calculates dynamic pricing based on localized market elasticity."""
    if supply <= 0:
        multiplier = 3.0
    else:
        ratio = demand / float(supply)
        if ratio <= 1.0:
            multiplier = 1.0
        else:
            multiplier = min(3.5, 1.0 + (ratio - 1.0) * 0.5)
    return round(base_fare * multiplier, 2)
