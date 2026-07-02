import logging
from datetime import datetime, timezone

import db
import openaq_client as openaq

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("ingest")


def ingest_station(station: dict):
    """Ambil data terbaru 1 station dari OpenAQ, simpan ke database."""
    station_id = station["id"]
    location_id = station["openaq_location_id"]
    name = station["station_name"]

    logger.info(f"[{name}] Mengambil data dari OpenAQ location_id={location_id} ...")

    # 1. Detail location -> untuk tahu sensorsId -> nama parameter
    location_detail = openaq.get_location(location_id)
    sensor_lookup = openaq.build_sensor_param_lookup(location_detail)

    if not sensor_lookup:
        logger.warning(f"[{name}] Tidak ada sensor ditemukan, skip.")
        return

    # 2. Nilai terbaru semua sensor di location tsb
    latest_response = openaq.get_location_latest(location_id)
    row = openaq.parse_latest_to_row(latest_response, sensor_lookup)

    if not row["measurement_time"] or not row["values"]:
        logger.warning(f"[{name}] Tidak ada data measurement baru, skip.")
        return

    # 3. Simpan ke air_quality_measurements
    #    aqi dibiarkan NULL karena OpenAQ pada endpoint ini tidak mengirim AQI,
    #    hanya konsentrasi polutan mentah (lihat penjelasan di README).
    new_id = db.insert_measurement(
        station_id=station_id,
        measurement_time=row["measurement_time"],
        values=row["values"],
        aqi=None,
    )

    if new_id:
        logger.info(f"[{name}] Tersimpan measurement id={new_id} @ {row['measurement_time']}")
    else:
        logger.info(f"[{name}] Data @ {row['measurement_time']} sudah ada sebelumnya (skip duplikat).")


def run_ingest_all():
    stations = db.get_active_stations()

    if not stations:
        logger.warning(
            "Belum ada station aktif di tabel `stations`. "
            "Tambahkan dulu lewat scripts/add_station.py"
        )
        return

    logger.info(f"Menjalankan ingest untuk {len(stations)} station aktif...")
    for station in stations:
        try:
            ingest_station(station)
        except Exception as e:
            logger.exception(f"Gagal ingest station id={station['id']}: {e}")

    logger.info("Selesai.")


if __name__ == "__main__":
    run_ingest_all()