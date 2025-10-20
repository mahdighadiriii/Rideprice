from enum import Enum


class WeatherType(str, Enum):
    CLEAR = "clear"
    RAIN = "rain"
    SNOW = "snow"


class TrafficLevel(str, Enum):
    NORMAL = "normal"
    LIGHT = "light"
    MODERATE = "moderate"
    HEAVY = "heavy"
