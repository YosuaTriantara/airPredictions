import numpy as np
from src.models.registry import registry
from src.models import lstm
from src.models import xgboost


class Predictor:
    
    def predict(self, processed: dict) -> float:
        lstm_input = processed["X_window"]                  
        xgb_last_features = processed["xgb_last_features"]  

        # tahap 1: LSTM -> prediksi AQI dalam skala asli
        lstm_prediction = lstm.predict(
            registry.lstm,
            registry.scaler_y,
            lstm_input
        )

        # tahap 2: gabungkan fitur terakhir (scaled) + prediksi LSTM (skala asli)
        xgb_input = np.hstack([
            xgb_last_features,
            [[lstm_prediction]]
        ])

        # tahap 3: XGBoost memprediksi residual/koreksi atas prediksi LSTM
        residual_prediction = xgboost.predict_residual(
            registry.xgboost,
            xgb_input
        )

        # tahap 4: hasil akhir = prediksi LSTM + koreksi residual
        final_prediction = lstm_prediction + residual_prediction
        return final_prediction

predictor = Predictor()
