from pathlib import Path
from src.inference.pipeline import pipeline


class PredictionService:

    def predict(self):
        csv_path = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "preprocessing"
            / "data.csv"
        )
        return pipeline.run(csv_path)


prediction_service = PredictionService()