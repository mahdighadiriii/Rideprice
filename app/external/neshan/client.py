import httpx

from app.core.config import settings
from app.core.exceptions import ExternalAPIException
from app.external.base_client import BaseHTTPClient
from app.external.neshan.models import NeshanRouteResult


class NeshanClient(BaseHTTPClient):
    def __init__(self):
        super().__init__(
            base_url=settings.NESHAN_BASE_URL, api_key=settings.NESHAN_API_KEY
        )

    async def get_route(
        self, origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float
    ) -> NeshanRouteResult:
        """
        Get route information from Neshan API

        Neshan API: GET /v4/direction
        Docs: https://platform.neshan.org/api/direction/
        """
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
