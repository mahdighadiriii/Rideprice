from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.request import PriceCalculationRequest
from app.api.v1.schemas.response import PriceCalculationResponse
from app.core.exceptions import CalculationException
from app.services.price_service import PriceService

router = APIRouter()
price_service = PriceService()


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
