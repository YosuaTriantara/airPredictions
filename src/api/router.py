from fastapi import APIRouter

from src.api.routes.health import router as health_router
from src.api.routes.prediction import router as prediction_router
from src.api.routes.measurement import router as measurement_router
from src.api.routes.station import router as station_router


api_router = APIRouter()

api_router.include_router(
    health_router
)

api_router.include_router(
    prediction_router
)

api_router.include_router(
    measurement_router
)

api_router.include_router(
    station_router
)
