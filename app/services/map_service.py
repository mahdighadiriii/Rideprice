from typing import Any, Dict

from app.external.google.client import GoogleMapsClient
from app.external.google.models import GoogleGeocodingResult, GoogleRouteResult
from app.external.neshan.client import NeshanClient
from app.external.neshan.models import NeshanGeocodingResult, NeshanRouteResult


class MapService:
    def __init__(self):
        self.neshan_client = NeshanClient()
        self.google_client = GoogleMapsClient()

    async def get_route_info(
        self, origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float
    ) -> NeshanRouteResult:
        """Get route information using Neshan API (default)"""
        return await self.neshan_client.get_route(
            origin_lat, origin_lon, dest_lat, dest_lon
        )

    async def get_route_info_google(
        self, origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float
    ) -> GoogleRouteResult:
        """Get route information using Google Maps API"""
        return await self.google_client.get_route(
            origin_lat, origin_lon, dest_lat, dest_lon
        )

    async def compare_routes(
        self, origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float
    ) -> Dict[str, Any]:
        """Compare routes from both Neshan and Google Maps"""

        import asyncio

        neshan_route, google_route = await asyncio.gather(
            self.neshan_client.get_route(origin_lat, origin_lon, dest_lat, dest_lon),
            self.google_client.get_route(origin_lat, origin_lon, dest_lat, dest_lon),
            return_exceptions=True,
        )

        neshan_error = isinstance(neshan_route, Exception)
        google_error = isinstance(google_route, Exception)

        result = {
            "neshan": {
                "available": not neshan_error,
                "distance_km": neshan_route.distance_km if not neshan_error else None,
                "time_minutes": neshan_route.time_minutes if not neshan_error else None,
                "error": str(neshan_route) if neshan_error else None,
            },
            "google": {
                "available": not google_error,
                "distance_km": google_route.distance_km if not google_error else None,
                "time_minutes": google_route.time_minutes if not google_error else None,
                "time_in_traffic_minutes": google_route.time_in_traffic_minutes
                if not google_error
                else None,
                "error": str(google_route) if google_error else None,
            },
        }

        if not neshan_error and not google_error:
            result["comparison"] = {
                "distance_diff_km": round(
                    abs(neshan_route.distance_km - google_route.distance_km), 2
                ),
                "time_diff_minutes": abs(
                    neshan_route.time_minutes - google_route.time_minutes
                ),
                "recommended_api": "google"
                if google_route.time_in_traffic_minutes < neshan_route.time_minutes
                else "neshan",
                "recommended_distance": min(
                    neshan_route.distance_km, google_route.distance_km
                ),
                "recommended_time": min(
                    neshan_route.time_minutes, google_route.time_in_traffic_minutes
                ),
            }

        return result

    async def geocode_address(self, address: str) -> NeshanGeocodingResult:
        """Convert address to coordinates (using OSM via Neshan client)"""
        return await self.neshan_client.geocode_address(address)

    async def geocode_address_google(self, address: str) -> GoogleGeocodingResult:
        """Convert address to coordinates using Google Geocoding"""
        return await self.google_client.geocode_address(address)
