import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import api_router
from src.models.registry import registry


app = FastAPI(
    title="AQI Prediction API",
    version="1.0.0"
)

_default_origins = "http://localhost:5173,http://127.0.0.1:5173"
_origins = os.getenv("CORS_ORIGINS", _default_origins).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():

    registry.initialize()


app.include_router(
    api_router,
    prefix="/api/v1"
)