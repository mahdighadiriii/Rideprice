from app.core.config import settings
from app.core.exceptions import ExternalAPIException
from app.external.base_client import BaseHTTPClient
from app.external.weather.models import WeatherResult
from app.models.enums import WeatherType


class WeatherClient(BaseHTTPClient):
    def __init__(self):
        super().__init__(
            base_url="https://api.openweathermap.org/data/2.5",
            api_key=settings.OPENWEATHER_API_KEY,
        )

    async def get_weather(self, lat: float, lon: float) -> WeatherResult:
        """Get current weather from OpenWeatherMap"""
        try:
            params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": "metric"}

            response = await self.get("/weather", params=params)

            if not response or "weather" not in response:
                raise ExternalAPIException("Invalid weather API response")

            weather_code = response["weather"][0]["id"]
            weather_desc = response["weather"][0]["description"]
            temp = response["main"]["temp"]

            weather_type = self._map_weather_code(weather_code)

            return WeatherResult(
                weather_type=weather_type, description=weather_desc, temperature=temp
            )

        except Exception as e:
            raise ExternalAPIException(f"Weather API error: {str(e)}")

    def _map_weather_code(self, code: int) -> WeatherType:
        """Map OpenWeatherMap codes to weather types"""
        if 600 <= code < 700:
            return WeatherType.SNOW
        elif 300 <= code < 600:
            return WeatherType.RAIN
        else:
            return WeatherType.CLEAR
