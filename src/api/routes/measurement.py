from fastapi import APIRouter
from fastapi import Depends

from src.api.dependencies import get_measurement_service

from src.services.measurement_service import MeasurementService

from src.api.responses import success


router = APIRouter(
    prefix="/measurement",
    tags=["Measurement"]
)


@router.get("/latest/{station_id}")
def latest(
    station_id: int,
    service: MeasurementService = Depends(
        get_measurement_service
    )
):

    data = service.latest(
        station_id
    )

    return success(data)


@router.get("/history/{station_id}")
def history(
    station_id: int,
    limit: int = 24,
    service: MeasurementService = Depends(
        get_measurement_service
    )
):

    data = service.history(
        station_id,
        limit
    )

    return success(data)
