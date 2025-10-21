from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.request import (
    PriceCalculationRequest,
    PriceCalculationWithAddressGoogleRequest,
    PriceCalculationWithAddressRequest,
    PriceCalculationWithRouteRequest,
    TrafficLevel,
)
from app.api.v1.schemas.response import PriceCalculationResponse
from app.core.exceptions import CalculationException, ExternalAPIException
from app.services.map_service import MapService
from app.services.price_service import PriceService
from app.services.weather_service import WeatherService

router = APIRouter()
price_service = PriceService()
map_service = MapService()
weather_service = WeatherService()


@router.post("/calculate", response_model=PriceCalculationResponse)
async def calculate_price(request: PriceCalculationRequest):
    """Calculate ride price with surge multiplier"""
    try:
        result = price_service.calculate_price(
            distance_km=request.distance_km,
            time_minutes=request.time_minutes,
            passengers=request.passengers_waiting,
            drivers=request.drivers_available,
            weather=request.weather.value,
            traffic=request.traffic.value,
            current_time=request.current_time,
        )
        return result
    except CalculationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/calculate-with-route", response_model=PriceCalculationResponse)
async def calculate_price_with_route(request: PriceCalculationWithRouteRequest):
    """Calculate ride price with automatic route and weather detection"""
    try:
        route_info = await map_service.get_route_info(
            origin_lat=request.origin_lat,
            origin_lon=request.origin_lon,
            dest_lat=request.dest_lat,
            dest_lon=request.dest_lon,
        )

        if request.weather is None:
            weather_type = await weather_service.get_weather_type(
                request.origin_lat, request.origin_lon
            )
        else:
            weather_type = request.weather

        result = price_service.calculate_price(
            distance_km=route_info.distance_km,
            time_minutes=route_info.time_minutes,
            passengers=request.passengers_waiting,
            drivers=request.drivers_available,
            weather=weather_type.value,
            traffic=request.traffic.value,
            current_time=request.current_time,
        )

        return result

    except ExternalAPIException as e:
        raise HTTPException(status_code=503, detail=f"External API error: {str(e)}")
    except CalculationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/calculate-with-address", response_model=PriceCalculationResponse)
async def calculate_price_with_address(request: PriceCalculationWithAddressRequest):
    try:
        origin = await map_service.geocode_address(request.origin_address)
        destination = await map_service.geocode_address(request.destination_address)
        route_info = await map_service.get_route_info(
            origin_lat=origin.latitude,
            origin_lon=origin.longitude,
            dest_lat=destination.latitude,
            dest_lon=destination.longitude,
        )
        if request.weather is None:
            weather_type = await weather_service.get_weather_type(
                origin.latitude, origin.longitude
            )
        else:
            weather_type = request.weather
        if request.traffic is None:
            duration_minutes = route_info.time_minutes
            distance_km = route_info.distance_km
            if duration_minutes / distance_km < 1.5:
                traffic_type = TrafficLevel.NORMAL
            elif duration_minutes / distance_km < 2.0:
                traffic_type = TrafficLevel.LIGHT
            elif duration_minutes / distance_km < 2.5:
                traffic_type = TrafficLevel.MODERATE
            else:
                traffic_type = TrafficLevel.HEAVY
        else:
            traffic_type = request.traffic
        result = price_service.calculate_price(
            distance_km=route_info.distance_km,
            time_minutes=route_info.time_minutes,
            passengers=request.passengers_waiting,
            drivers=request.drivers_available,
            weather=weather_type.value,
            traffic=traffic_type.value,
            current_time=request.current_time,
        )
        return result
    except ExternalAPIException as e:
        raise HTTPException(status_code=503, detail=f"External API error: {str(e)}")
    except CalculationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/compare-routes-with-address")
async def compare_routes_with_address(origin_address: str, destination_address: str):
    """Compare routes using address inputs"""
    try:
        origin = await map_service.geocode_address(origin_address)
        destination = await map_service.geocode_address(destination_address)

        comparison = await map_service.compare_routes(
            origin_lat=origin.latitude,
            origin_lon=origin.longitude,
            dest_lat=destination.latitude,
            dest_lon=destination.longitude,
        )

        comparison["origin"] = {
            "address": origin.address,
            "coordinates": {"lat": origin.latitude, "lon": origin.longitude},
        }
        comparison["destination"] = {
            "address": destination.address,
            "coordinates": {"lat": destination.latitude, "lon": destination.longitude},
        }

        return comparison

    except ExternalAPIException as e:
        raise HTTPException(status_code=503, detail=f"External API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@router.post("/calculate-with-address-google", response_model=PriceCalculationResponse)
async def calculate_price_with_address_google(
    request: PriceCalculationWithAddressGoogleRequest,
):
    """
    Calculate ride price using Google Maps API
    - Uses Google Maps for routing and real-time traffic
    - Auto-detects traffic level from Google's duration_in_traffic
    - Uses OpenWeather for weather (Google doesn't provide weather in Directions API)
    """
    try:
        origin = await map_service.geocode_address_google(request.origin_address)
        destination = await map_service.geocode_address_google(
            request.destination_address
        )

        route_info = await map_service.get_route_info_google(
            origin_lat=origin.latitude,
            origin_lon=origin.longitude,
            dest_lat=destination.latitude,
            dest_lon=destination.longitude,
        )

        if request.weather is None:
            weather_type = await weather_service.get_weather_type(
                origin.latitude, origin.longitude
            )
        else:
            weather_type = request.weather

        if request.traffic is None:
            duration_with_traffic = route_info.time_in_traffic_minutes
            duration_without_traffic = route_info.time_minutes
            distance_km = route_info.distance_km

            traffic_ratio = (
                duration_with_traffic / duration_without_traffic
                if duration_without_traffic > 0
                else 1.0
            )

            if traffic_ratio <= 1.1:
                traffic_type = TrafficLevel.NORMAL
            elif traffic_ratio <= 1.3:
                traffic_type = TrafficLevel.LIGHT
            elif traffic_ratio <= 1.6:
                traffic_type = TrafficLevel.MODERATE
            else:
                traffic_type = TrafficLevel.HEAVY
        else:
            traffic_type = request.traffic

        result = price_service.calculate_price(
            distance_km=route_info.distance_km,
            time_minutes=route_info.time_in_traffic_minutes,
            passengers=request.passengers_waiting,
            drivers=request.drivers_available,
            weather=weather_type.value,
            traffic=traffic_type.value,
            current_time=request.current_time,
        )

        return result

    except ExternalAPIException as e:
        raise HTTPException(status_code=503, detail=f"External API error: {str(e)}")
    except CalculationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
