import joblib
import pandas as pd

from .features import FEATURE_COLS 


def load_scaler(scaler_path: str):
    return joblib.load(scaler_path)


def scale_features(df_features: pd.DataFrame, scaler_path: str) -> pd.DataFrame:

    scaler = load_scaler(scaler_path)

    missing = [c for c in FEATURE_COLS if c not in df_features.columns]
    if missing:
        raise ValueError(f"Kolom fitur hilang, cek features.py: {missing}")

    df = df_features[FEATURE_COLS].copy()
    # sisa NaN biasanya dari periode awal rolling/lag sebelum data cukup panjang
    df = df.dropna(subset=FEATURE_COLS)

    scaled = scaler.transform(df)
    return pd.DataFrame(scaled, index=df.index, columns=FEATURE_COLS)