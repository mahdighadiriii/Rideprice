from typing import Optional

from pydantic import BaseModel


class GoogleRouteResult(BaseModel):
    distance_km: float
    time_minutes: int
    time_in_traffic_minutes: int
    original_response: Optional[dict] = None


class GoogleGeocodingResult(BaseModel):
    latitude: float
    longitude: float
    address: str
    place_id: str
