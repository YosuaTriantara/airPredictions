from fastapi import FastAPI
from src.api.router import api_router
from src.models.registry import registry


app = FastAPI(
    title="AQI Prediction API",
    version="1.0.0"
)


@app.on_event("startup")
def startup():

    registry.initialize()


app.include_router(
    api_router,
    prefix="/api/v1"
)