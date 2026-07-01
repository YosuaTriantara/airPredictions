from pydantic import BaseModel


class PredictRequest(BaseModel):

    station_id: int