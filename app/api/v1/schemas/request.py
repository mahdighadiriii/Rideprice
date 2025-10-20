from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import TrafficLevel, WeatherType


class PriceCalculationRequest(BaseModel):
    distance_km: float = Field(..., gt=0, description="Distance in kilometers")
    time_minutes: int = Field(..., gt=0, description="Estimated time in minutes")
    passengers_waiting: int = Field(
        ..., ge=0, description="Number of waiting passengers"
    )
    drivers_available: int = Field(..., gt=0, description="Number of available drivers")
    weather: WeatherType = Field(..., description="Weather condition")
    traffic: TrafficLevel = Field(..., description="Traffic level")
    current_time: datetime = Field(
        default_factory=datetime.now, description="Current time"
    )
