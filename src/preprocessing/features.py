import numpy as np
import pandas as pd

ROLLING_COLS = ["PM2.5", "PM10", "NO2", "CO", "O3"]
ROLLING_WINDOWS = [3, 6, 24]

FEATURE_COLS = [
    "PM2.5", "PM10", "NO", "NO2", "NOx", "CO", "SO2", "O3",
    "hour_sin", "hour_cos", "month_sin", "month_cos", "is_weekend",
    "PM2.5_roll3", "PM2.5_roll6", "PM2.5_roll24",
    "PM10_roll3", "PM10_roll6", "PM10_roll24",
    "NO2_roll3", "NO2_roll6", "NO2_roll24",
    "CO_roll3", "CO_roll6", "CO_roll24",
    "O3_roll3", "O3_roll6", "O3_roll24",
    "PM2.5_lag1", "PM2.5_lag3",
]


def add_cyclic_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    hour = df.index.hour
    month = df.index.month
    dayofweek = df.index.dayofweek

    df["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    df["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    df["month_sin"] = np.sin(2 * np.pi * month / 12)
    df["month_cos"] = np.cos(2 * np.pi * month / 12)
    df["is_weekend"] = (dayofweek >= 5).astype(int)
    return df


def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ROLLING_COLS:
        for w in ROLLING_WINDOWS:
            df[f"{col}_roll{w}"] = df[col].rolling(w, min_periods=1).mean()
    return df


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """PM2.5_lag1/3: shift biasa dari data aktual."""
    df = df.copy()
    df["PM2.5_lag1"] = df["PM2.5"].shift(1)
    df["PM2.5_lag3"] = df["PM2.5"].shift(3)
    return df


def build_features(df_clean: pd.DataFrame) -> pd.DataFrame:
    """Entry point features.py: DataFrame bersih -> DataFrame + 30 fitur final."""
    df = add_cyclic_time_features(df_clean)
    df = add_rolling_features(df)
    df = add_lag_features(df)
    return df