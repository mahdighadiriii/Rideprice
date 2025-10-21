from datetime import datetime
from typing import Optional

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


class PriceCalculationWithRouteRequest(BaseModel):
    origin_lat: float = Field(..., ge=-90, le=90, description="Origin latitude")
    origin_lon: float = Field(..., ge=-180, le=180, description="Origin longitude")
    dest_lat: float = Field(..., ge=-90, le=90, description="Destination latitude")
    dest_lon: float = Field(..., ge=-180, le=180, description="Destination longitude")
    passengers_waiting: int = Field(
        ..., ge=0, description="Number of waiting passengers"
    )
    drivers_available: int = Field(..., gt=0, description="Number of available drivers")
    weather: Optional[WeatherType] = Field(
        None, description="Weather (auto-detected if not provided)"
    )
    traffic: TrafficLevel = Field(..., description="Traffic level")
    current_time: datetime = Field(
        default_factory=datetime.now, description="Current time"
    )


class PriceCalculationWithAddressRequest(BaseModel):
    origin_address: str = Field(
        ..., min_length=3, description="Origin address or place name"
    )
    destination_address: str = Field(
        ..., min_length=3, description="Destination address or place name"
    )
    passengers_waiting: int = Field(
        ..., ge=0, description="Number of waiting passengers"
    )
    drivers_available: int = Field(..., gt=0, description="Number of available drivers")
    weather: Optional[WeatherType] = Field(
        None, description="Weather (auto-detected if not provided)"
    )
    traffic: Optional[TrafficLevel] = Field(
        None, description="Traffic level (auto-detected if not provided)"
    )
    current_time: datetime = Field(
        default_factory=datetime.now, description="Current time"
    )


class RouteComparisonRequest(BaseModel):
    origin_lat: float = Field(..., ge=-90, le=90, description="Origin latitude")
    origin_lon: float = Field(..., ge=-180, le=180, description="Origin longitude")
    dest_lat: float = Field(..., ge=-90, le=90, description="Destination latitude")
    dest_lon: float = Field(..., ge=-180, le=180, description="Destination longitude")


class PriceCalculationWithAddressGoogleRequest(BaseModel):
    origin_address: str = Field(
        ..., min_length=3, description="Origin address or place name"
    )
    destination_address: str = Field(
        ..., min_length=3, description="Destination address or place name"
    )
    passengers_waiting: int = Field(
        ..., ge=0, description="Number of waiting passengers"
    )
    drivers_available: int = Field(..., gt=0, description="Number of available drivers")
    weather: Optional[WeatherType] = Field(
        None, description="Weather (auto-detected if not provided)"
    )
    traffic: Optional[TrafficLevel] = Field(
        None, description="Traffic level (auto-detected from Google Maps traffic data)"
    )
    current_time: datetime = Field(
        default_factory=datetime.now, description="Current time"
    )
