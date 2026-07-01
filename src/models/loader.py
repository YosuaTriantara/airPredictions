from pathlib import Path
import json
import joblib
from tensorflow.keras.models import load_model


ARTIFACT_PATH = Path("artifacts")


class ModelLoader:
    @staticmethod
    def load_lstm():
        return load_model(
            ARTIFACT_PATH / "models" / "best_lstm.keras"
        )

    @staticmethod
    def load_xgboost():
        return joblib.load(
            ARTIFACT_PATH / "models" / "best_xgb.pkl"
        )

    @staticmethod
    def load_scaler_X():
        return joblib.load(
            ARTIFACT_PATH / "scaler_X.pkl"
        )

    @staticmethod
    def load_scaler_y():
        return joblib.load(
            ARTIFACT_PATH / "scaler_y.pkl"
        )

    @staticmethod
    def load_category_mapping():
        with open(
            ARTIFACT_PATH / "metadata" / "category_mapping.json",
            encoding="utf-8"
        ) as f:
            return json.load(f)