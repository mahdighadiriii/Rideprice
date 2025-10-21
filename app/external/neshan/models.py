from typing import Optional

from pydantic import BaseModel


class NeshanLocation(BaseModel):
    lat: float
    lng: float


class NeshanRouteResponse(BaseModel):
    distance: int
    duration: int


class NeshanRouteResult(BaseModel):
    distance_km: float
    time_minutes: int
    original_response: Optional[dict] = None


class NeshanGeocodingLocation(BaseModel):
    x: float
    y: float


class NeshanGeocodingItem(BaseModel):
    title: str
    address: str
    location: NeshanGeocodingLocation


class NeshanGeocodingResult(BaseModel):
    latitude: float
    longitude: float
    address: str
    title: str
