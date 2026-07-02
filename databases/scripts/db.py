import os
import logging
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "sslmode": os.getenv("DB_SSLMODE", "require"),
}


@contextmanager
def get_connection():
    """Context manager: buka koneksi, commit/rollback otomatis, lalu tutup."""
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL)
    else:
        conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def get_cursor(dict_cursor=True):
    """Context manager: langsung dapat cursor siap pakai."""
    with get_connection() as conn:
        cursor_factory = psycopg2.extras.RealDictCursor if dict_cursor else None
        cur = conn.cursor(cursor_factory=cursor_factory)
        try:
            yield cur
        finally:
            cur.close()


def get_active_stations():
    """Ambil semua station yang is_active = TRUE."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT id, openaq_location_id, station_name, city
            FROM stations
            WHERE is_active = TRUE
            ORDER BY id;
            """
        )
        return cur.fetchall()


def upsert_station(openaq_location_id, station_name, country, city, latitude, longitude):
    """Insert station baru, atau update kalau openaq_location_id sudah ada."""
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO stations
                (openaq_location_id, station_name, country, city, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (openaq_location_id) DO UPDATE SET
                station_name = EXCLUDED.station_name,
                country      = EXCLUDED.country,
                city         = EXCLUDED.city,
                latitude     = EXCLUDED.latitude,
                longitude    = EXCLUDED.longitude,
                updated_at   = NOW()
            RETURNING id;
            """,
            (openaq_location_id, station_name, country, city, latitude, longitude),
        )
        return cur.fetchone()["id"]


def insert_measurement(station_id, measurement_time, values: dict, aqi=None):
    """
    Insert satu baris pengukuran ke air_quality_measurements.
    `values` = dict dengan key: pm25, pm10, no, no2, nox, co, so2, o3
    Duplikat (station_id, measurement_time) akan di-skip (ON CONFLICT DO NOTHING).
    """
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO air_quality_measurements
                (station_id, measurement_time, pm25, pm10, no, no2, nox, co, so2, o3, aqi)
            VALUES
                (%(station_id)s, %(measurement_time)s, %(pm25)s, %(pm10)s, %(no)s,
                 %(no2)s, %(nox)s, %(co)s, %(so2)s, %(o3)s, %(aqi)s)
            ON CONFLICT (station_id, measurement_time) DO NOTHING
            RETURNING id;
            """,
            {
                "station_id": station_id,
                "measurement_time": measurement_time,
                "pm25": values.get("pm25"),
                "pm10": values.get("pm10"),
                "no": values.get("no"),
                "no2": values.get("no2"),
                "nox": values.get("nox"),
                "co": values.get("co"),
                "so2": values.get("so2"),
                "o3": values.get("o3"),
                "aqi": aqi,
            },
        )
        row = cur.fetchone()
        return row["id"] if row else None


def insert_prediction(station_id, model_name, predicted_aqi, category, prediction_time=None):
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


def insert_model_log(prediction_id, status, error_message=None):
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


def get_last_n_rows(station_id: int, n: int = 24):
    """Ambil N baris terakhir untuk sebuah station -> siap jadi DataFrame."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT measurement_time, pm25, pm10, no, no2, nox, co, so2, o3, aqi
            FROM air_quality_measurements
            WHERE station_id = %s
            ORDER BY measurement_time DESC
            LIMIT %s;
            """,
            (station_id, n),
        )
        return cur.fetchall()
