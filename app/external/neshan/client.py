import httpx

from app.core.config import settings
from app.core.exceptions import ExternalAPIException
from app.external.base_client import BaseHTTPClient
from app.external.neshan.models import NeshanGeocodingResult, NeshanRouteResult


class NeshanClient(BaseHTTPClient):
    def __init__(self):
        super().__init__(
            base_url=settings.NESHAN_BASE_URL, api_key=settings.NESHAN_API_KEY
        )

    async def get_route(
        self, origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float
    ) -> NeshanRouteResult:
        """Get route information from Neshan API"""
        try:
            params = {
                "type": "car",
                "origin": f"{origin_lat},{origin_lon}",
                "destination": f"{dest_lat},{dest_lon}",
            }

            response = await self.get("/direction", params=params)

            if not response or "routes" not in response:
                raise ExternalAPIException("Invalid response from Neshan API")

            route = response["routes"][0]
            legs = route["legs"][0]

            distance_meters = legs["distance"]["value"]
            duration_seconds = legs["duration"]["value"]

            return NeshanRouteResult(
                distance_km=distance_meters / 1000,
                time_minutes=int(duration_seconds / 60),
                original_response=response,
            )

        except httpx.HTTPError as e:
            raise ExternalAPIException(f"Neshan API error: {str(e)}")
        except Exception as e:
            raise ExternalAPIException(f"Failed to get route: {str(e)}")

    async def geocode_address(self, address: str) -> NeshanGeocodingResult:
        """
        Convert address to coordinates using OpenStreetMap Nominatim
        Works with English AND Persian addresses!
        FREE - No API key needed!
        """
        try:
            search_term = address
            if "tehran" not in address.lower() and "تهران" not in address:
                search_term = f"{address}, Tehran, Iran"

            params = {
                "q": search_term,
                "format": "json",
                "limit": 1,
                "countrycodes": "ir",
            }

            headers = {
                "User-Agent": "RidePrice-Service/1.0",
                "Accept-Language": "fa,en",
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://nominatim.openstreetmap.org/search",
                    headers=headers,
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()

            if not data or len(data) == 0:
                raise ExternalAPIException(f"Address not found: {address}")

            result = data[0]

            return NeshanGeocodingResult(
                latitude=float(result["lat"]),
                longitude=float(result["lon"]),
                address=result.get("display_name", address),
                title=result.get("name", ""),
            )

        except httpx.HTTPError as e:
            raise ExternalAPIException(f"Geocoding error: {str(e)}")
        except Exception as e:
            raise ExternalAPIException(f"Failed to geocode address: {str(e)}")
