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
