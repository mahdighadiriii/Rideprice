from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "RidePrice Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    BASE_FARE: int = 35000
    TIME_RATE: int = 2500
    DISTANCE_RATE: int = 6000
    MAX_SURGE: float = 2.5

    NESHAN_API_KEY: str = ""
    NESHAN_BASE_URL: str = "https://api.neshan.org/v4"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
