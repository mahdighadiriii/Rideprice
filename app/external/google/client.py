import httpx

from app.core.config import settings
from app.core.exceptions import ExternalAPIException
from app.external.base_client import BaseHTTPClient
from app.external.google.models import GoogleGeocodingResult, GoogleRouteResult


class GoogleMapsClient(BaseHTTPClient):
    def __init__(self):
        super().__init__(
            base_url="https://maps.googleapis.com/maps/api",
            api_key=settings.GOOGLE_MAPS_API_KEY,
        )

    async def get_route(
        self, origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float
    ) -> GoogleRouteResult:
        """Get route information from Google Maps Directions API"""
        try:
            params = {
                "origin": f"{origin_lat},{origin_lon}",
                "destination": f"{dest_lat},{dest_lon}",
                "mode": "driving",
                "departure_time": "now",
                "traffic_model": "best_guess",
                "key": self.api_key,
            }

            response = await self.get("/directions/json", params=params)

            if response.get("status") != "OK":
                raise ExternalAPIException(
                    f"Google Maps API error: {response.get('status')}"
                )

            route = response["routes"][0]
            leg = route["legs"][0]

            distance_meters = leg["distance"]["value"]
            duration_seconds = leg["duration"]["value"]

            duration_in_traffic = leg.get("duration_in_traffic", {}).get(
                "value", duration_seconds
            )

            return GoogleRouteResult(
                distance_km=distance_meters / 1000,
                time_minutes=int(duration_seconds / 60),
                time_in_traffic_minutes=int(duration_in_traffic / 60),
                original_response=response,
            )

        except httpx.HTTPError as e:
            raise ExternalAPIException(f"Google Maps API error: {str(e)}")
        except Exception as e:
            raise ExternalAPIException(f"Failed to get route: {str(e)}")

    async def geocode_address(self, address: str) -> GoogleGeocodingResult:
        """Convert address to coordinates using Google Geocoding API"""
        try:
            search_term = address
            if "tehran" not in address.lower() and "تهران" not in address:
                search_term = f"{address}, Tehran, Iran"

            params = {
                "address": search_term,
                "key": self.api_key,
            }

            response = await self.get("/geocode/json", params=params)

            if response.get("status") != "OK":
                raise ExternalAPIException(
                    f"Geocoding failed: {response.get('status')}"
                )

            result = response["results"][0]
            location = result["geometry"]["location"]

            return GoogleGeocodingResult(
                latitude=location["lat"],
                longitude=location["lng"],
                address=result["formatted_address"],
                place_id=result.get("place_id", ""),
            )

        except httpx.HTTPError as e:
            raise ExternalAPIException(f"Google Geocoding error: {str(e)}")
        except Exception as e:
            raise ExternalAPIException(f"Failed to geocode address: {str(e)}")
