from app.external.weather.client import WeatherClient
from app.external.weather.models import WeatherResult
from app.models.enums import WeatherType


class WeatherService:
    def __init__(self):
        self.weather_client = WeatherClient()

    async def get_current_weather(self, lat: float, lon: float) -> WeatherResult:
        """Get current weather for location"""
        return await self.weather_client.get_weather(lat, lon)

    async def get_weather_type(self, lat: float, lon: float) -> WeatherType:
        """Get only weather type (for price calculation)"""
        result = await self.weather_client.get_weather(lat, lon)
        return result.weather_type
