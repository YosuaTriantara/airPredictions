from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd

from .cleaner import clean_openaq_csv, clean_openaq_df
from .features import build_features
from .scaler import scale_features
from .window import build_window, WINDOW_SIZE


def run_preprocessing_pipeline(
    data: Union[str, Path, pd.DataFrame],
    scaler,
    window_size: int = WINDOW_SIZE,
    convert_ppb: bool = False,
) -> dict:
    """
    Entry point tunggal buat pipeline inference. Tahapannya harus tetap sinkron
    dengan notebook training:

        1. cleaning        -> cleaner.py       (sama pola dgn notebook 01-03)
        2. feature eng.    -> features.py      (30 fitur, sama dgn notebook 04)
        3. scaling         -> scaler.py        (scaler_X hasil fit di notebook 05,
                                                 JANGAN fit ulang saat inference)
        4. windowing       -> window.py        (window_size=24, sama dgn notebook 05)

    Parameters
    ----------
    data   : path CSV mentah OpenAQ (long format), ATAU DataFrame long-format yang
             sudah diambil dari database (mis. hasil repository.get_last_24_hours).
             Kalau str/Path -> dibaca lewat clean_openaq_csv.
             Kalau DataFrame -> langsung lewat clean_openaq_df (tanpa baca file).
    scaler : instance scaler_X yang sudah dimuat (disarankan lewat registry, supaya
             tidak baca ulang .pkl tiap request), atau path ke file .pkl-nya.
    window_size : default 24, HARUS sama dengan saat training.
    convert_ppb : lihat catatan di cleaner.convert_units -- default False.

    Returns
    -------
    dict:
        X_window          : np.ndarray (1, window_size, 30) -> input predictor tahap 1 (LSTM)
        xgb_last_features : np.ndarray (1, 30) -> fitur timestep terakhir (scaled),
                             dipakai sebagai bagian input predictor tahap 2 (XGBoost),
                             lihat notebook 07: X_train_xgb = X_train[:, -1, :]
        df_features       : pd.DataFrame fitur sebelum scaling, untuk debugging/inspeksi
    """
    if isinstance(data, pd.DataFrame):
        df_clean = clean_openaq_df(data, convert_ppb=convert_ppb)
    else:
        df_clean = clean_openaq_csv(data, convert_ppb=convert_ppb)

    df_features = build_features(df_clean)
    df_scaled = scale_features(df_features, scaler)
    X_window = build_window(df_scaled, window_size=window_size)

    xgb_last_features = X_window[:, -1, :]

    return {
        "X_window": X_window,
        "xgb_last_features": xgb_last_features,
        "df_features": df_features,
    }


if __name__ == "__main__":
    from .scaler import load_scaler

    scaler_X = load_scaler("../artifacts/scaler_X.pkl")

    result = run_preprocessing_pipeline(
        data="preprocessing/data.csv",
        scaler=scaler_X,
    )
    print("X_window shape:", result["X_window"].shape)
    print("xgb_last_features shape:", result["xgb_last_features"].shape)
    print(result["df_features"].tail(3))
