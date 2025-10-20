from fastapi import FastAPI

from app.api.v1.endpoints import health, price
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Intelligent taxi pricing micro-service",
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(price.router, prefix="/api/v1/price", tags=["Price Calculation"])


@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }
