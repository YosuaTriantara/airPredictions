from fastapi import APIRouter
from fastapi import Depends

from src.api.dependencies import get_station_service
from src.services.station_service import StationService
from src.api.responses import success


router = APIRouter(
    prefix="/station",
    tags=["Station"]
)


@router.get("/")
def stations(
    service: StationService = Depends(
        get_station_service
    )
):

    return success(
        service.all()
    )


@router.get("/{station_id}")
def detail(
    station_id: int,
    service: StationService = Depends(
        get_station_service
    )
):

    return success(
        service.detail(
            station_id
        )
    )
