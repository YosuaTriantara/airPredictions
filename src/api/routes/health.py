from fastapi import APIRouter

from src.api.responses import success


router = APIRouter()


@router.get("/health")
def health():

    return success(
        {
            "status": "healthy"
        }
    )