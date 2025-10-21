from app.external.neshan.client import NeshanClient
from app.external.neshan.models import NeshanRouteResult


class MapService:
    def __init__(self):
        self.neshan_client = NeshanClient()

    async def get_route_info(
        self, origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float
    ) -> NeshanRouteResult:
        """Get route information using Neshan API"""
        return await self.neshan_client.get_route(
            origin_lat, origin_lon, dest_lat, dest_lon
        )
