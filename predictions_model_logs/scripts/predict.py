"""
predict.py
Contoh alur ketika user menekan tombol "Predict" (lihat diagram di PDF):

    Frontend -> POST /predict
             -> SELECT last 24 rows
             -> DataFrame
             -> Preprocessing -> Scaling -> Window -> LSTM
             -> Prediction
             -> simpan ke tabel `predictions`
             -> log ke `model_logs`

File ini hanya kerangka (skeleton) integrasi database + logging.
Bagian load_model() / preprocess() / model.predict() perlu diisi
sesuai model LSTM kamu sendiri (mis. file .h5 / .keras yang sudah dilatih
dengan feature_cols = [PM2.5, PM10, NO, NO2, NOx, CO, SO2, O3]).
"""

import logging
import pandas as pd

import db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("predict")

FEATURE_COLS = ["pm25", "pm10", "no", "no2", "nox", "co", "so2", "o3"]

AQI_CATEGORY_BINS = [
    (0, 50, "Good"),
    (51, 100, "Moderate"),
    (101, 150, "Unhealthy for Sensitive Groups"),
    (151, 200, "Unhealthy"),
    (201, 300, "Very Unhealthy"),
    (301, 500, "Hazardous"),
]


def categorize_aqi(aqi_value: float) -> str:
    for low, high, label in AQI_CATEGORY_BINS:
        if low <= aqi_value <= high:
            return label
    return "Unknown"


def load_last_24h(station_id: int) -> pd.DataFrame:
    rows = db.get_last_n_rows(station_id, n=24)
    df = pd.DataFrame(rows)
    return df.sort_values("measurement_time").reset_index(drop=True)


def preprocess(df: pd.DataFrame):
    """
    TODO: sesuaikan dengan preprocessing yang dipakai saat training
    (imputasi NaN, scaling dengan scaler yang sama, windowing, dsb).
    """
    X = df[FEATURE_COLS].fillna(method="ffill").fillna(method="bfill")
    return X


def run_prediction(station_id: int, model_name: str = "lstm_v1"):
    """
    Jalankan satu siklus prediksi untuk sebuah station dan simpan hasilnya.
    Dipanggil dari endpoint POST /predict di API/backend kamu.
    """
    prediction_id = None
    try:
        df = load_last_24h(station_id)

        if len(df) < 24:
            raise ValueError(
                f"Data tidak cukup untuk prediksi (butuh 24 baris, ada {len(df)})."
            )

        X = preprocess(df)

        # ---- TODO: ganti bagian ini dengan model LSTM asli ----
        # model = load_model("model.keras")
        # X_scaled = scaler.transform(X)
        # X_window = X_scaled.reshape(1, 24, len(FEATURE_COLS))
        # predicted_aqi = float(model.predict(X_window)[0][0])
        predicted_aqi = float(X.mean().mean())  # placeholder sementara
        # ---------------------------------------------------------

        category = categorize_aqi(predicted_aqi)

        prediction_id = db.insert_prediction(
            station_id=station_id,
            model_name=model_name,
            predicted_aqi=predicted_aqi,
            category=category,
        )
        db.insert_model_log(prediction_id=prediction_id, status="success")

        logger.info(
            f"Station {station_id}: predicted_aqi={predicted_aqi:.1f} ({category}) "
            f"tersimpan sebagai prediction_id={prediction_id}"
        )
        return {"prediction_id": prediction_id, "predicted_aqi": predicted_aqi, "category": category}

    except Exception as e:
        logger.exception(f"Prediksi gagal untuk station {station_id}: {e}")
        db.insert_model_log(prediction_id=prediction_id, status="failed", error_message=str(e))
        raise


if __name__ == "__main__":
    import sys

    station_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    run_prediction(station_id)