import argparse
import csv
import logging
from collections import defaultdict
from datetime import datetime

import db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed_from_csv")

VALID_PARAMS = {"pm25", "pm10", "no", "no2", "nox", "co", "so2", "o3"}


def parse_dt(value: str) -> datetime:
    # contoh: "2026-07-01T00:15:00Z"
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def read_csv_rows(csv_path: str):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        raise ValueError(f"File CSV kosong: {csv_path}")
    return rows


def build_station_info(rows, station_name_override=None, city_override=None):
    first = rows[0]
    return {
        "openaq_location_id": int(first["location_id"]),
        "station_name": station_name_override or first["location_name"],
        "country": first.get("country_iso") or None,
        "city": city_override or (first.get("location_name", "").split(",")[-1].split("-")[0].strip() or None),
        "latitude": float(first["latitude"]) if first.get("latitude") else None,
        "longitude": float(first["longitude"]) if first.get("longitude") else None,
    }


def group_by_timestamp(rows):
    """long-format -> {datetime: {param: value}}"""
    grouped = defaultdict(dict)
    for row in rows:
        param = row["parameter"].strip().lower()
        if param not in VALID_PARAMS:
            continue  # parameter di luar 8 fitur, skip (mis. relativehumidity dsb.)
        value = row["value"]
        if value in (None, ""):
            continue
        dt = parse_dt(row["datetimeUtc"])
        grouped[dt][param] = float(value)
    return grouped


def seed(csv_path: str, station_name_override=None, city_override=None):
    rows = read_csv_rows(csv_path)
    station_info = build_station_info(rows, station_name_override, city_override)

    station_id = db.upsert_station(**station_info)
    logger.info(
        f"Station siap: db_id={station_id}, openaq_location_id={station_info['openaq_location_id']}, "
        f"nama={station_info['station_name']}"
    )

    grouped = group_by_timestamp(rows)
    logger.info(f"Ditemukan {len(grouped)} timestamp unik di CSV, mulai insert...")

    inserted, skipped = 0, 0
    for dt in sorted(grouped.keys()):
        values = grouped[dt]
        new_id = db.insert_measurement(
            station_id=station_id,
            measurement_time=dt,
            values=values,
            aqi=None,
        )
        if new_id:
            inserted += 1
        else:
            skipped += 1  # sudah ada (duplikat), kena ON CONFLICT DO NOTHING

    logger.info(f"Selesai. Inserted={inserted}, Skipped(duplikat)={skipped}, Total={len(grouped)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path ke file CSV export OpenAQ")
    parser.add_argument("--station-name", default=None, help="Override nama station")
    parser.add_argument("--city", default=None, help="Override kota")
    args = parser.parse_args()

    seed(args.csv, station_name_override=args.station_name, city_override=args.city)
