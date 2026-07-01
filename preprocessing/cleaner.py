import pandas as pd

# Konversi ppb -> ug/m3 pada kondisi standar (25 C, 1 atm): ug/m3 = ppb * MW / 24.45
MOLAR_MASS = {
    "co": 28.01,
    "no": 30.01,
    "no2": 46.0055,
    "nox": 46.0055,  # NOx dilaporkan setara NO2
    "so2": 64.066,
}

OPENAQ_TO_TRAIN_COLS = {
    "pm25": "PM2.5",
    "pm10": "PM10",
    "no": "NO",
    "no2": "NO2",
    "nox": "NOx",
    "co": "CO",
    "so2": "SO2",
    "o3": "O3",
}



def convert_units(df_long: pd.DataFrame, convert_ppb: bool = False) -> pd.DataFrame:
    """Konversi baris berunit ppb ke ug/m3 (khusus CO ke mg/m3)."""
    df = df_long.copy()
    if not convert_ppb:
        return df

    is_ppb = df["unit"].str.lower() == "ppb"

    for param, mw in MOLAR_MASS.items():
        mask = is_ppb & (df["parameter"] == param)
        df.loc[mask, "value"] = df.loc[mask, "value"] * mw / 24.45

    # CO training dalam mg/m3, bukan ug/m3 -> bagi 1000 setelah konversi di atas
    co_mask = df["parameter"] == "co"
    df.loc[co_mask, "value"] = df.loc[co_mask, "value"] / 1000.0

    return df


def pivot_to_wide(df_long: pd.DataFrame) -> pd.DataFrame:
    """Long (1 baris/polutan) -> wide (1 baris/waktu, polutan jadi kolom)."""
    df = df_long.copy()
    df["datetime"] = pd.to_datetime(df["datetimeLocal"]).dt.tz_localize(None)

    df_wide = df.pivot_table(
        index="datetime", columns="parameter", values="value", aggfunc="mean"
    )
    df_wide = df_wide.rename(columns=OPENAQ_TO_TRAIN_COLS)
    return df_wide


def resample_hourly(df_wide: pd.DataFrame) -> pd.DataFrame:
    """OpenAQ ~15 menit -> training per jam, jadi diagregasi mean per jam."""
    return df_wide.sort_index().resample("1h").mean()


def add_missing_pollutants(df_hourly: pd.DataFrame) -> pd.DataFrame:
    return df_hourly.copy()


def impute_missing_values(df_hourly: pd.DataFrame) -> pd.DataFrame:
    """3-stage imputation, sama pola dengan pipeline training:
    ffill/bfill (limit 2 jam) -> interpolasi waktu -> median kolom (fallback terakhir)."""
    df = df_hourly.copy()
    df = df.ffill(limit=2).bfill(limit=2)
    df = df.interpolate(method="time")
    df = df.fillna(df.median(numeric_only=True))
    return df


def _load_openaq_data(path: str) -> pd.DataFrame:
    """
    >>> TITIK YANG DIGANTI KALAU PINDAH DARI CSV KE DATABASE <<<

    Sekarang: baca file CSV export OpenAQ.
    Nanti (production): ganti isi fungsi ini jadi query ke database, dan
    ubah parameter `path` jadi apa pun yang dibutuhkan (mis. location_id,
    start_time, end_time, connection). Selama return-nya tetap DataFrame
    long-format dengan kolom yang sama (parameter, value, unit,
    datetimeLocal, ...), sisa fungsi di file ini (dan features.py,
    scaler.py, window.py, pipeline.py) TIDAK perlu diubah sama sekali.

    Contoh nanti:
        def _load_openaq_data(location_id, start_time, end_time, conn):
            query = '''SELECT parameter, value, unit, datetimeLocal
                       FROM measurements
                       WHERE location_id = %s AND datetimeLocal BETWEEN %s AND %s'''
            return pd.read_sql(query, conn, params=[location_id, start_time, end_time])
    """
    return pd.read_csv(path)


def clean_openaq_csv(path: str, convert_ppb: bool = False) -> pd.DataFrame:
    df_long = _load_openaq_data(path)
    df_long = convert_units(df_long, convert_ppb=convert_ppb)
    df_wide = pivot_to_wide(df_long)
    df_hourly = resample_hourly(df_wide)
    df_hourly = add_missing_pollutants(df_hourly)
    df_hourly = impute_missing_values(df_hourly)
    return df_hourly