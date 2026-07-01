from typing import Tuple

import numpy as np
import pandas as pd

from .cleaner import clean_openaq_csv
from .features import build_features
from .scaler import scale_features
from .window import build_window, WINDOW_SIZE

SCALER_X_PATH = "artifacts/scaler_X.pkl"


def run_preprocessing_pipeline(
    openaq_csv_path: str,
    scaler_path: str = SCALER_X_PATH,
    window_size: int = WINDOW_SIZE,
    convert_ppb: bool = False,
) -> Tuple[np.ndarray, pd.DataFrame]:
    """
    Entry point tunggal buat pipeline inference.

    Parameters
    ----------
    openaq_csv_path : path CSV mentah dari OpenAQ (format long, hasil export/API).
                       Titik ganti CSV -> DB ada di cleaner._load_openaq_data(),
                       bukan di sini -- fungsi ini tidak perlu berubah nanti.
    scaler_path       : path ke artifacts/scaler_X.pkl HASIL RETRAIN dengan 30 fitur
                         (scaler lama 36-fitur sudah tidak kompatibel, lihat scaler.py).
    window_size       : default 24, harus sama dengan saat training
    convert_ppb       : lihat catatan di cleaner.convert_units -- default False.

    Returns
    -------
    X_window : np.ndarray shape (1, window_size, 30) -> input model.predict()
    df_features : pd.DataFrame fitur sebelum scaling, untuk debugging/inspeksi.
    """
    df_clean = clean_openaq_csv(openaq_csv_path, convert_ppb=convert_ppb)
    df_features = build_features(df_clean)
    df_scaled = scale_features(df_features, scaler_path)
    X_window = build_window(df_scaled, window_size=window_size)
    return X_window, df_features


if __name__ == "__main__":
    # Jalankan dari root project: python -m preprocessing.pipeline
    X_window, df_features = run_preprocessing_pipeline(
        openaq_csv_path="preprocessing/data.csv",
    )
    print("X_window shape:", X_window.shape)
    print(df_features.tail(3))