from fastapi import APIRouter
from fastapi import Depends
from src.api.schemas.prediction import PredictRequest
from src.api.dependencies import get_prediction_service
from src.services.prediction_service import PredictionService
from src.api.responses import success


router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)


@router.post("/")
def predict(
    request: PredictRequest,
    service: PredictionService = Depends(get_prediction_service)
):
    result = service.predict(request.station_id)
    return success(result)
