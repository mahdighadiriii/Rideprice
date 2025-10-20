from datetime import datetime

from app.core.constants import BASE_FARE, DISTANCE_RATE, TIME_RATE
from app.services.surge_service import SurgeService


class PriceService:
    def __init__(self):
        self.surge_service = SurgeService()

    def calculate_price(
        self,
        distance_km: float,
        time_minutes: int,
        passengers: int,
        drivers: int,
        weather: str,
        traffic: str,
        current_time: datetime,
    ) -> dict:
        """Calculate final price with surge"""

        base_fare = BASE_FARE
        time_cost = time_minutes * TIME_RATE
        distance_cost = int(distance_km * DISTANCE_RATE)
        subtotal = base_fare + time_cost + distance_cost

        surge_info = self.surge_service.calculate_surge(
            passengers, drivers, weather, traffic, current_time
        )

        final_price = int(subtotal * surge_info["surge_multiplier"])

        return {
            "base_fare": base_fare,
            "time_cost": time_cost,
            "distance_cost": distance_cost,
            "subtotal": subtotal,
            "surge_calculation": surge_info,
            "final_price": final_price,
            "price_locked": True,
        }
