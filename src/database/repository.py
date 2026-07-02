from typing import Optional

import pandas as pd

from src.database.connection import get_cursor

POLLUTANT_COLUMNS = ["pm25", "pm10", "no", "no2", "nox", "co", "so2", "o3"]


class RepositoryError(Exception):
    """Dilempar kalau data yang dibutuhkan tidak tersedia di database."""


def get_all_stations():
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT id, openaq_location_id, station_name, country, city,
                   latitude, longitude, is_active, created_at, updated_at
            FROM stations
            ORDER BY id;
            """
        )
        return cur.fetchall()


def get_station(station_id: int):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT id, openaq_location_id, station_name, country, city,
                   latitude, longitude, is_active, created_at, updated_at
            FROM stations
            WHERE id = %s;
            """,
            (station_id,),
        )
        return cur.fetchone()


def get_latest(station_id: int):
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT measurement_time, pm25, pm10, no, no2, nox, co, so2, o3, aqi
            FROM air_quality_measurements
            WHERE station_id = %s
            ORDER BY measurement_time DESC
            LIMIT 1;
            """,
            (station_id,),
        )
        return cur.fetchone()


def get_history(station_id: int, limit: int = 24):
    """N baris terakhir untuk sebuah station, wide format (buat endpoint /measurement/history)."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT measurement_time, pm25, pm10, no, no2, nox, co, so2, o3, aqi
            FROM air_quality_measurements
            WHERE station_id = %s
            ORDER BY measurement_time DESC
            LIMIT %s;
            """,
            (station_id, limit),
        )
        rows = cur.fetchall()
        return list(reversed(rows))  # urut waktu naik


def get_measurements_since(station_id: int, hours: int):
    """
    Semua baris dalam `hours` jam terakhir (relatif terhadap measurement_time
    paling baru milik station itu, BUKAN terhadap NOW() server, supaya tetap
    benar walau ingest sempat berhenti/telat).
    """
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT measurement_time, pm25, pm10, no, no2, nox, co, so2, o3, aqi
            FROM air_quality_measurements
            WHERE station_id = %s
              AND measurement_time >= (
                  SELECT MAX(measurement_time) - (%s || ' hours')::interval
                  FROM air_quality_measurements
                  WHERE station_id = %s
              )
            ORDER BY measurement_time ASC;
            """,
            (station_id, hours, station_id),
        )
        return cur.fetchall()


def get_last_24_hours(station_id: int, window_hours: int = 48) -> pd.DataFrame:
    """
    Ambil data `window_hours` jam terakhir (default 48, bukan 24!) lalu ubah
    dari wide -> long format, siap dipakai langsung oleh
    `src.preprocessing.pipeline.run_preprocessing_pipeline`.

    Kenapa window_hours default-nya lebih besar dari 24:
    data OpenAQ granularitasnya ~15 menit, lalu di-resample jadi per-jam
    (`resample_hourly`), dan fitur lag (`PM2.5_lag3`) + rolling butuh
    beberapa jam pemanasan sebelum baris pertama valid (non-NaN). Ambil
    24 baris MENTAH (bukan 24 jam) tidak akan cukup -- baru cover ~6 jam
    dan setelah resample+dropna bisa tersisa cuma segelintir baris.
    Ambil berdasarkan RENTANG WAKTU (jam), bukan jumlah baris, supaya window
    LSTM (butuh 24 baris jam berturut-turut) selalu terpenuhi selama data
    di DB memang cukup rapat (idealnya <=15-30 menit per titik).

    Return kolom: parameter, value, unit, datetimeLocal
    """
    rows = get_measurements_since(station_id, hours=window_hours)

    if not rows:
        raise RepositoryError(
            f"Tidak ada data pengukuran untuk station_id={station_id}."
        )

    df_wide = pd.DataFrame(rows)

    df_long = df_wide.melt(
        id_vars=["measurement_time"],
        value_vars=[c for c in POLLUTANT_COLUMNS if c in df_wide.columns],
        var_name="parameter",
        value_name="value",
    )
    df_long["unit"] = "µg/m³"
    df_long["datetimeLocal"] = df_long["measurement_time"]
    df_long["datetimeUtc"] = df_long["measurement_time"]
    df_long = df_long.dropna(subset=["value"])

    n_hours_covered = pd.to_datetime(df_wide["measurement_time"]).dt.floor("h").nunique()
    if n_hours_covered < 27:  # 24 window + buffer kasar utk lag3/rolling warm-up
        raise RepositoryError(
            f"Data station_id={station_id} dalam {window_hours} jam terakhir cuma "
            f"mencakup ~{n_hours_covered} jam unik (perlu >=27 setelah resample per-jam). "
            "Perbesar window_hours atau pastikan ingest tidak ada gap besar."
        )

    return df_long[["parameter", "value", "unit", "datetimeLocal", "datetimeUtc"]]


def insert_prediction(
    station_id: int,
    model_name: str,
    predicted_aqi: float,
    category: str,
    prediction_time: Optional[str] = None,
):
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO predictions (station_id, prediction_time, model_name, predicted_aqi, category)
            VALUES (%s, COALESCE(%s, NOW()), %s, %s, %s)
            RETURNING id;
            """,
            (station_id, prediction_time, model_name, predicted_aqi, category),
        )
        return cur.fetchone()["id"]


def insert_model_log(prediction_id: Optional[int], status: str, error_message: Optional[str] = None):
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO model_logs (prediction_id, status, error_message)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (prediction_id, status, error_message),
        )
        return cur.fetchone()["id"]


class Repository:
    get_all_station = staticmethod(get_all_stations)
    get_station = staticmethod(get_station)
    get_latest = staticmethod(get_latest)
    get_history = staticmethod(get_history)
    get_last_24_hours = staticmethod(get_last_24_hours)
    insert_prediction = staticmethod(insert_prediction)
    insert_model_log = staticmethod(insert_model_log)


repository = Repository()
