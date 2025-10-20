import math
from datetime import datetime

from app.core.constants import (
    MAX_SURGE_MULTIPLIER,
    NIGHT_TIME_END,
    NIGHT_TIME_FACTOR,
    NIGHT_TIME_START,
    TRAFFIC_FACTORS,
    WEATHER_FACTORS,
)


class SurgeService:
    @staticmethod
    def calculate_surge(
        passengers: int,
        drivers: int,
        weather: str,
        traffic: str,
        current_time: datetime,
    ) -> dict:
        """Calculate surge multiplier"""

        surge = 1.0

        demand_factor = 0
        if drivers > 0:
            ratio = passengers / drivers
            if ratio > 1.0:
                demand_factor = math.log10(ratio)

        weather_factor = WEATHER_FACTORS.get(weather.lower(), 0)

        traffic_factor = TRAFFIC_FACTORS.get(traffic.lower(), 0)

        night_factor = 0
        hour = current_time.hour
        if NIGHT_TIME_START <= hour < NIGHT_TIME_END:
            night_factor = NIGHT_TIME_FACTOR

        total = surge + demand_factor + weather_factor + traffic_factor + night_factor

        final_surge = min(total, MAX_SURGE_MULTIPLIER)

        return {
            "base_multiplier": 1.0,
            "demand_factor": round(demand_factor, 2),
            "weather_factor": weather_factor,
            "traffic_factor": traffic_factor,
            "night_factor": night_factor,
            "total_before_cap": round(total, 2),
            "surge_multiplier": round(final_surge, 2),
            "is_capped": total > MAX_SURGE_MULTIPLIER,
        }
