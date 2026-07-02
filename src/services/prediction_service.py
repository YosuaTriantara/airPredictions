import logging
from src.database.repository import repository
from src.inference.pipeline import pipeline

logger = logging.getLogger(__name__)


class PredictionService:

    def predict(self, station_id: int):
        prediction_id = None
        try:
            df_long = repository.get_last_24_hours(station_id)
            result = pipeline.run(df_long)

            prediction_id = repository.insert_prediction(
                station_id=station_id,
                model_name="lstm_xgb_v1",
                predicted_aqi=result["aqi"],
                category=result["category"],
                prediction_time=result["prediction_time"],
            )
            repository.insert_model_log(prediction_id=prediction_id, status="success")

            result["station_id"] = station_id
            result["prediction_id"] = prediction_id
            return result

        except Exception as e:
            logger.exception(f"Prediksi gagal untuk station_id={station_id}: {e}")
            repository.insert_model_log(
                prediction_id=prediction_id,
                status="failed",
                error_message=str(e),
            )
            raise


prediction_service = PredictionService()
