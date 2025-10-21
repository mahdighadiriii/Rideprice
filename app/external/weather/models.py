from pydantic import BaseModel

from app.models.enums import WeatherType


class WeatherCondition(BaseModel):
    id: int
    main: str
    description: str


class WeatherAPIResponse(BaseModel):
    weather: list[WeatherCondition]


class WeatherResult(BaseModel):
    weather_type: WeatherType
    description: str
    temperature: float
