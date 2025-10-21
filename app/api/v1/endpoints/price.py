from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.request import (
    PriceCalculationRequest,
    PriceCalculationWithRouteRequest,
)
from app.api.v1.schemas.response import PriceCalculationResponse
from app.core.exceptions import CalculationException, ExternalAPIException
from app.services.map_service import MapService
from app.services.price_service import PriceService

router = APIRouter()
price_service = PriceService()
map_service = MapService()


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
    """Calculate ride price by fetching route info from Neshan API"""
    try:
        route_info = await map_service.get_route_info(
            origin_lat=request.origin_lat,
            origin_lon=request.origin_lon,
            dest_lat=request.dest_lat,
            dest_lon=request.dest_lon,
        )

        result = price_service.calculate_price(
            distance_km=route_info.distance_km,
            time_minutes=route_info.time_minutes,
            passengers=request.passengers_waiting,
            drivers=request.drivers_available,
            weather=request.weather.value,
            traffic=request.traffic.value,
            current_time=request.current_time,
        )

        return result

    except ExternalAPIException as e:
        raise HTTPException(status_code=503, detail=f"Map service error: {str(e)}")
    except CalculationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
