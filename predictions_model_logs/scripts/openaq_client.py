"""
openaq_client.py
Wrapper tipis di atas OpenAQ API v3 (butuh API key, header X-API-Key).
Docs: https://docs.openaq.org/
"""

import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = os.getenv("OPENAQ_BASE_URL", "https://api.openaq.org/v3")
API_KEY = os.getenv("OPENAQ_API_KEY")

HEADERS = {"X-API-Key": API_KEY} if API_KEY else {}

# Mapping nama parameter OpenAQ -> nama kolom database kita
PARAM_MAP = {
    "pm25": "pm25",
    "pm10": "pm10",
    "no": "no",
    "no2": "no2",
    "nox": "nox",
    "co": "co",
    "so2": "so2",
    "o3": "o3",
}


def _get(path, params=None):
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def search_locations(city=None, country=None, limit=100):
    """Cari location di OpenAQ (untuk mengisi tabel `stations` pertama kali)."""
    params = {"limit": limit}
    if city:
        params["city"] = city
    if country:
        params["iso"] = country
    return _get("/locations", params=params)


def get_location(location_id: int):
    """Detail satu location by id."""
    return _get(f"/locations/{location_id}")


def get_location_latest(location_id: int):
    """
    Ambil nilai terbaru semua sensor pada satu location.
    Response: {"results": [{"datetime": {...}, "value": ..., "sensorsId": ..., "parameter": {...}}, ...]}
    """
    return _get(f"/locations/{location_id}/latest")


def parse_latest_to_row(latest_response: dict, sensor_param_lookup: dict) -> dict:
    """
    Ubah response /locations/{id}/latest menjadi satu baris siap insert.

    sensor_param_lookup: dict {sensorsId: parameter_name} yang didapat
    dari endpoint /locations/{id} (field sensors[].parameter.name),
    karena /latest sendiri hanya mengembalikan sensorsId + value + datetime.

    Return:
        {
            "measurement_time": "2026-06-30T09:00:00+00:00",
            "values": {"pm25": 20, "pm10": 33, ...},
        }
    Kalau ada beberapa datetime berbeda antar sensor, dipakai yang paling baru.
    """
    results = latest_response.get("results", [])
    values = {}
    latest_dt = None

    for item in results:
        sensor_id = item.get("sensorsId")
        param_name = sensor_param_lookup.get(sensor_id)
        if param_name not in PARAM_MAP:
            continue  # parameter di luar 8 fitur yang kita pakai, skip

        col = PARAM_MAP[param_name]
        values[col] = item.get("value")

        dt = item.get("datetime", {}).get("utc")
        if dt and (latest_dt is None or dt > latest_dt):
            latest_dt = dt

    return {"measurement_time": latest_dt, "values": values}


def build_sensor_param_lookup(location_detail: dict) -> dict:
    """
    Dari response get_location(), bangun {sensorsId: parameter_name}.
    """
    lookup = {}
    results = location_detail.get("results", [])
    if not results:
        return lookup

    sensors = results[0].get("sensors", [])
    for s in sensors:
        sensor_id = s.get("id")
        param_name = s.get("parameter", {}).get("name")
        if sensor_id is not None and param_name:
            lookup[sensor_id] = param_name

    return lookup