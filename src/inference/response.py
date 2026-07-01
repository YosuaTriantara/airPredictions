from datetime import datetime
from src.inference.category import get_category


def build_response(prediction: float):

    return {
        "prediction_time": datetime.utcnow().isoformat(),
        "aqi": round(prediction, 2),
        "category": get_category(prediction)
    }