from pydantic import BaseModel


class SurgeCalculation(BaseModel):
    base_multiplier: float
    demand_factor: float
    weather_factor: float
    traffic_factor: float
    night_factor: float
    total_before_cap: float
    surge_multiplier: float
    is_capped: bool


class PriceCalculationResponse(BaseModel):
    base_fare: int
    time_cost: int
    distance_cost: int
    subtotal: int
    surge_calculation: SurgeCalculation
    final_price: int
    price_locked: bool
